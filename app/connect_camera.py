# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module Camera connet
# Description: Connect,send,capturn,video
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------

from shared_queue import queue_process_capture_detect
from obj_log import safe_put_queue,debug_print
from folder_create import Create
from pypylon import pylon
import cv2
import time
import base64
import threading
import traceback
import os
import queue

class BaslerCamera:

    """Lớp kết nối và điều khiển camera Basler sử dụng pypylon."""
    foler = Create()
    VIDEO_IMAGE_QUALITY = 50  # chất lượng hình ảnh video gửi lên
    SET_TIME_TAKE_IMG = 1000 # set thời gian chờ lấy ảnh từ camera (ms)

    def __init__(self,queue_wait = None ,emit_func=None,config_file = None):

        self.camera = None
        self.converter = None
        self.emit_func = emit_func  # Hàm để gửi dữ liệu qua SocketIO (nếu có)
        self.config_file = config_file
        self.queue = queue_wait
        self.lock = threading.Lock()

        self.sender_thread = None
        self.queue_send_video = None
        self._emit_running = False
        self.open_send_video = False
        self.flag_open_thread = True
    
    def enable_send_video(self):
        """Hàm bật luồng gửi video"""
        self.open_send_video = True

    def disable_send_video(self):
        """Hàm tắt luồng gửi video"""
        self.open_send_video = False

    def initialize_camera(self):
        """
        Khởi tạo camera Basler:
        - Nếu config_file tồn tại -> load cấu hình từ file
        - Nếu không -> dump config mặc định hiện tại ra file
        - Nếu chưa kết nối camera, sẽ thử lại mỗi 2 giây
        """
        try:
            tl_factory = pylon.TlFactory.GetInstance()
            self.camera = None

            # Loop liên tục dò camera
            if self.camera is None:
                try:
                    self.camera = pylon.InstantCamera(tl_factory.CreateFirstDevice())
                except Exception as e:
                    debug_print(f"⚠️ Chưa tìm thấy camera Basler ({e}), thử lại sau 2 giây...")
                    time.sleep(2)  # chờ 2 giây trước khi thử lại
                    return
            self.camera.Open()
            # Nếu có file config -> load
            if self.config_file and os.path.exists(self.config_file):
                # Có file -> load từ file xuống camera
                debug_print(f"🔹 Loading camera config from {self.config_file}")
                pylon.FeaturePersistence.Load(self.config_file, self.camera.GetNodeMap(), True)

                # Sau khi load, nếu bạn muốn đảm bảo camera đang dùng config đó thì không cần làm gì thêm.
                # Nếu muốn "save lại" (cập nhật file nếu có thay đổi nhỏ) thì có thể thêm:
                # pylon.FeaturePersistence.Save(self.config_file, self.camera.GetNodeMap())

            else:
                # Không có file -> dump config hiện tại của camera ra file
                debug_print("⚡ No config file found, using current camera settings and saving...")
                if self.config_file:
                    try:
                        pylon.FeaturePersistence.Save(self.config_file, self.camera.GetNodeMap())
                        debug_print(f"💾 Saved current camera config to {self.config_file}")
                    except Exception as e:
                        debug_print(f"❌ Không thể save config: {e}")

            self.show_camera_info()
            # Chuẩn bị converter sang BGR8 để OpenCV xử lý         
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

            debug_print("✅ Camera initialized successfully")
        except:
            debug_print("Cau hinh loi cam")

    def show_camera_info(self):
            """Hiển thị thông tin camera Basler."""
            device_info = self.camera.GetDeviceInfo()
            debug_print("  Model Name:", device_info.GetModelName())
            debug_print("  Serial Number:", device_info.GetSerialNumber())
            debug_print("  Vendor Name:", device_info.GetVendorName())
            debug_print("  Device Class:", device_info.GetDeviceClass())
    def _emit_loop(self):
        """Luồng gửi ảnh liên tục qua SocketIO."""
        while self._emit_running:
            try:
                jpg_as_text = None
                if not self.queue_send_video.empty():
                    frame = self.queue_send_video.get_nowait()
                    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY),BaslerCamera.VIDEO_IMAGE_QUALITY])
                    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                    if jpg_as_text:
                        self.emit_func.emit(
                            'camera_frame',
                            {'image': jpg_as_text},
                            namespace='/video'
                        )
                time.sleep(1/40)
            except Exception as e:
                time.sleep(1)
                debug_print(f"Lỗi gửi ảnh: {e}")

    def start_emit_loop(self):
        """Khởi động Luông gửi ảnh liên tục qua SocketIO."""
        if not self._emit_running:
            self._emit_running = True
            self.sender_thread = threading.Thread(target=self._emit_loop, daemon=True)
            self.sender_thread.start()
            debug_print("✅ Emit loop thread started")
    def stop_emit_loop(self):
            """Dừng luồng gửi ảnh"""
            if self._emit_running:
                debug_print("🛑 Stopping emit loop...")
                self._emit_running = False
                if self.sender_thread and self.sender_thread.is_alive():
                    self.sender_thread.join(timeout=2)
                debug_print("✅ Emit loop thread stopped")  

    def start_stream(self):
        """Gửi video liên tục từ camera qua SocketIO.Chụp ảnh theo yêu cầu từ queue."""
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.last_emit_time = time.time()
        self.min_emit_interval = 1/40
        self.queue_send_video = queue.Queue(maxsize=2)    
        safe_put_queue({"type":"software","level":"info","data":f"Camera được mở thành công"})
        while self.camera.IsGrabbing():
            if self.open_send_video:
                if self.flag_open_thread:
                    self.start_emit_loop()
                    self.flag_open_thread = False
            else:
                self.flag_open_thread = True # Bat bien flag chuan bi cho lan chay tiep theo chi can  self.open_send_video on la mo lai duoc luong
                self.stop_emit_loop()
            grabResult = self.camera.RetrieveResult(BaslerCamera.SET_TIME_TAKE_IMG,pylon.TimeoutHandling_Return)
            if grabResult.GrabSucceeded():
                now = time.time()
                image_cv = self.converter.Convert(grabResult)
                frame = image_cv.GetArray()
                if self.emit_func and (now - self.last_emit_time) >= self.min_emit_interval and self.open_send_video:
                    # print("sO LUONG QUEUE TRONG QUEUE LA",self.queue_send_video.qsize())
                    # print("put vao trong queue")
                    if not self.queue_send_video.full():
                        self.queue_send_video.put(frame)
                    else:
                        # Nếu queue đã đầy thì bỏ frame cũ, thay bằng frame mới
                        try:
                            self.queue_send_video.get_nowait()
                        except queue.Empty:
                            pass
                        self.queue_send_video.put(frame)  
                self.last_emit_time = now
                if self.queue.qsize() > 0:
                        data = self.queue.get()
                        training     = data.get("training", -1)
                        name_capture  = data.get("name_capture", -1)
                        capture_detect = data.get("capture_detect",-1)
                        if training == 3:
                            if  name_capture != -1:
                                self.capture_one_frame_path(name_capture)
                            if capture_detect!= -1:
                                debug_print("Chụp ảnh nhận diện")
                                try:
                                    queue_process_capture_detect.put(frame,block=True,timeout=1)
                                except:
                                    debug_print("Queue đầy không chụp được ảnh")
            grabResult.Release()
            time.sleep(0.001)
        debug_print("Camera chưa sẵn sàng chạy khởi động")
        time.sleep(1)

    def show_camera_window(self):
        """Hiển thị cửa sổ video từ camera Basler."""
        try:
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            while self.camera.IsGrabbing():
                grabResult = self.camera.RetrieveResult(BaslerCamera.SET_TIME_TAKE_IMG, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()

                    height, width, _ = frame.shape
                    small_frame = cv2.resize(frame, (int(width / 4), int(height / 4)))
                    cv2.imshow("Camera Feed", small_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        # img = self.capture_one_frame()
                        # cv2.imshow("anh",img)
                        # cv2.waitKey(0)  # Nhấn phím bất kỳ để đóng cửa sổ
                        # cv2.destroyAllWindows()
                        # print("👉 Đã chụp ảnh theo yêu cầu.")
                        break            

                else:
                    debug_print("Lỗi khi chụp:", grabResult.ErrorCode, grabResult.ErrorDescription)

                grabResult.Release()
        except:
            debug_print("Chua ket noi duoc cam nen khong show dc thong tin")

    def capture_one_frame_path(self, save_path: str = None):
        """
        Chụp một ảnh từ camera và trả về frame (numpy array).
        Nếu save_path được cung cấp, sẽ lưu ảnh vào đường dẫn đó.
        Trả về frame nếu thành công, None nếu lỗi.
        """
        with self.lock:
            if self.camera is None or not self.camera.IsOpen():
                debug_print("❌ Camera chưa khởi tạo hoặc không mở được.")
                return None

            if not self.camera.IsGrabbing():
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            try:
                grabResult = self.camera.RetrieveResult(
                    BaslerCamera.SET_TIME_TAKE_IMG,
                    pylon.TimeoutHandling_ThrowException
                )
                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()
                    grabResult.Release()

                    if frame is None or frame.size == 0:
                        debug_print("❌ Ảnh rỗng, không lấy được frame.")
                        return None
                    # Nếu có đường dẫn lưu, lưu ảnh ngay
                    if save_path:
                        try:
                            ok = cv2.imwrite(save_path, frame)
                            if ok:
                                debug_print(f"📸 Đã lưu ảnh: {save_path}")
                            else:
                                debug_print(f"❌ Lưu ảnh thất bại: {save_path}")
                        except Exception as e:
                            debug_print(f"❌ Lỗi khi lưu ảnh: {e}")

                    return frame  # trả về frame numpy array
                else:
                    debug_print("❌ Lỗi khi chụp ảnh:", grabResult.ErrorCode, grabResult.ErrorDescription)
                    grabResult.Release()
                    return None

            except Exception as e:
                debug_print(f"⚠️ Lỗi khi lấy ảnh từ camera: {e}")
                traceback.print_exc()
                return None
            
    def capture_one_frame(self):
        """
        Chụp một ảnh từ camera và trả về frame (numpy array).
        Trả về None nếu lỗi hoặc không lấy được ảnh.
        Hàm này để test nhanh mà chạy để thử chụp ảnh từ camera.
        """
        with self.lock:
            if self.camera is None or not self.camera.IsOpen():
                debug_print("❌ Camera chưa khởi tạo hoặc không mở được.")
                return None

            if not self.camera.IsGrabbing():
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            try:
                grabResult = self.camera.RetrieveResult(
                    BaslerCamera.SET_TIME_TAKE_IMG,
                    pylon.TimeoutHandling_ThrowException
                )
                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()
                    grabResult.Release()

                    if frame is None or frame.size == 0:
                        debug_print("❌ Ảnh rỗng, không lấy được frame.")
                        return None

                    return frame  # ✅ Trả về ảnh dưới dạng numpy array
                else:
                    debug_print("❌ Lỗi khi chụp ảnh:", grabResult.ErrorCode, grabResult.ErrorDescription)
                    grabResult.Release()
                    return None

            except Exception as e:
                debug_print(f"⚠️ Lỗi khi lấy ảnh từ camera: {e}")
                traceback.print_exc()
                return None
            
    def release(self):
        """Hàm này để giải phóng tài nguyên camera khi không dùng nữa."""
        debug_print("Đang dừng camera...")
        if self.sender_thread:
            self.sender_thread.join(timeout=1)  # đợi thread kết thúc
        if self.camera:  
            self.camera.StopGrabbing()
            self.camera.Close()
        cv2.destroyAllWindows()
        debug_print("Đã giải phóng tài nguyên camera.")


    def run_cam(self):
        """Chạy hiển thị cửa sổ camera Basler. window"""
        self.initialize_camera()
        try:
            self.show_camera_window()
        except :
            debug_print("Lỗi pylon:1")
            self.initialize_camera()

    def run_cam_html(self):
        """Chạy gửi video qua SocketIO bật khi mở phẩn mềm"""
        try:
            self.show_camera_info()
            self.start_stream()
        except:
            debug_print("Lỗi pylon:2")
            self.initialize_camera()
           
    def is_camera_stable(self):
        """
        Kiểm tra camera có đang hoạt động hay không.
        Tránh conflict với luồng start_stream (không gọi RetrieveResult nữa).
        """
        try:
            if self.camera is None:
                debug_print("❌ Camera chưa khởi tạo.")
                return False

            if not self.camera.IsOpen():
                debug_print("❌ Camera chưa mở.")
                return False

            if self.camera.IsGrabbing():
                # Camera đang grabbing (có thể từ start_stream)
                # debug_print("✅ Camera đang chạy (luồng start_stream hoạt động).")
                return True
            else:
                debug_print("⚠️ Camera đã mở nhưng chưa grabbing.")
                return False

        except Exception as e:
            debug_print(f"⚠️ Lỗi khi kiểm tra camera: {e}")
            return False
        
    def show_file_config(self):
        """  Đọc file cấu hình camera Basler và trả về các thông số chính gửi thông tin lên giao diện người dùng."""
        path_file_config = BaslerCamera.foler.get_path_same_level("Camera_25129678.pfs")
        if path_file_config and self.camera is not None:
            data_file_config = BaslerCamera.foler.read_file_in_path(path_file_config)
            device_info = self.camera.GetDeviceInfo()

            # Lấy các giá trị từ file config
            frame = self.get_parameter_value(data_file_config, "AcquisitionFrameRateAbs")
            width = self.get_parameter_value(data_file_config, "Width")
            height = self.get_parameter_value(data_file_config, "Height")
            exposure = self.get_parameter_value(data_file_config, "ExposureTime")  # ví dụ thêm ExposureTime
            gain = self.get_parameter_value(data_file_config, "Gain")  # ví dụ thêm Gain
 
            # Lấy thêm thông tin camera từ DeviceInfo
            model = device_info.GetModelName()
            serial = device_info.GetSerialNumber()
            vendor = device_info.GetVendorName()
            device_class = device_info.GetDeviceClass()

            # Trả về tất cả thông tin dưới dạng dictionary
            return {
                "frame": frame,
                "width": width,
                "height": height,
                "exposure": exposure,
                "gain": gain,
                "model": model,
                "serial": serial,
                "vendor": vendor,
                "device_class": device_class
            }
        return False

    def get_parameter_value(self,data, parameter_name):
        """
        From the text data 'data', find 'parameter_name' and return its value.
        Each line format: ParameterName\tValue
        """
        if not data:
            return None

        # Split data into lines
        for line in data.splitlines():
            # Remove leading/trailing whitespace
            line = line.strip()
            # Check if the line starts with the parameter name
            if line.startswith(parameter_name):
                # Split by whitespace or tab
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]  # value
        return None
    

#==================================Hàm chạy kiểm thử====================================================#

# def main():
#     cam = BaslerCamera(config_file="Camera_25129678.pfs")
#     # print(cam.is_camera_stable())
#     # datawew= cam.show_file_config()
#     # print(datawew)
#     print(cam.show_file_config())
#     cam.run_cam()
# if __name__ == "__main__":
#     main()
