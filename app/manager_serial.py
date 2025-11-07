
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module manager serial com
# Description: Manager serial com
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
import threading
import time
import queue
import shared_queue
from obj_log import safe_put_queue,debug_print

class ManagerSerial:
    safe_put_queue({"type":"software","level":"info","data":f"COM chưa được mở"})
    def __init__(self,queue_rx_arm=None,queue_tx_arm=None):
        from serial_communication import Serial_Com 
        # Khởi tạo lớp giao tiếp Serial
        self.serial_com = Serial_Com()
        
        self.com_is_open = False
        # Hàng đợi gửi / nhận
        self.tx_queue = queue_tx_arm
        self.rx_queue = queue_rx_arm

        # Cờ chạy luồng
        self.running_tx = True
        self.running_rx = True
        self.running_check_connect = True
        

        self.rx_thread = threading.Thread(target=self._check_connect,daemon=True, name="check_connect_com")
        self.rx_thread.start()

        self.show_log = None # Cho phép hiên thị 1 lần log
        self.handshake_status = None  # trạng thái handshake

        self.mode_device = "normal" 
    def open_thread_receive_and_send(self):
    
        self.running_rx = True
        self.running_tx = True

        debug_print("✅ Mở 2 luồng nhận gửi dữ liệu")
        self.rx_thread = threading.Thread(target=self._listen_serial,daemon=True, name="SerialListener")
        self.rx_thread.start()

        self.tx_thread = threading.Thread(target=self._send_serial,daemon = True, name="SerialSender")
        self.tx_thread.start()

    def set_handshake_status(self, value):
        """Gán giá trị cho handshake_status"""
        self.handshake_status = value

    def get_handshake_status(self):
        """Lấy giá trị handshake_status hiện tại"""
        return self.handshake_status
    
    def close_thread_receive_and_send(self):
        # Dừng các luồng
        debug_print("🛑 Đang dừng luồng gửi nhận dữ liệu tới COM")

        # Đặt cờ chạy về False để các luồng thoát vòng lặp
        self.running_rx = False
        self.running_tx = False
        self.serial_com.ser = None
        self.serial_com.port = None
        # Nếu luồng đang chạy, join để đảm bảo đã kết thúc
        if hasattr(self, 'rx_thread') and self.rx_thread.is_alive():
            self.rx_thread.join(timeout=1)
            debug_print("✅ Luồng nhận dữ liệu đã dừng")

        if hasattr(self, 'tx_thread') and self.tx_thread.is_alive():
            self.tx_thread.join(timeout=1)
            debug_print("✅ Luồng gửi dữ liệu đã dừng")
        self.clear_rx_queue()
        self.clear_tx_queue()
        debug_print("✅ Đã dừng thành công.")
        safe_put_queue({"type":"software","level":"info","data":f"Đóng luồng nghe nhận STM32"})
    def _check_connect(self):
        safe_put_queue({"type":"software","level":"info","data":f"Mở luồng check COM"})
        flag = False
        while self.running_check_connect:
            exists, busy = self.serial_com.is_com_busy(self.serial_com.port)
            if not exists:  # neu k ton tai 
                self.com_is_open = False #trạng thái không mở
                if flag:
                    safe_put_queue({"type":"software","level":"error","data":"Cổng COM đóng"})
                    flag = False
                    self.close_thread_receive_and_send()
                # debug_print("[Check COM] Cố gắng mở lại cổng com khi com mất kết nối")
            elif exists and busy: #neu ban
                # debug_print("[Check COM] Cổng COM đang hoạt động bình thường")
                pass
            elif exists and not busy: # tồn tại nhưng không bật
                debug_print("[Check COM] Tìm thấy cổng COM cần kết nối tiến hành mở cổng")
                if not self.serial_com.ser:
                    status = self.serial_com.open_port()
                    if status:
                        flag =  True
                        debug_print("[Check COM] Mở cổng com thành công")
                        self.com_is_open = True   #bật cờ trạng thái lên
                        self.open_thread_receive_and_send()  #mở luồng nhận gửi để nhận tín hiệu
                    else:
                        debug_print("[Check COM] Mở cổng thất bại")
            time.sleep(1)

    def update_com(self,name_port,baudrate):
        if not self.com_is_open:
            status_open_com = self.serial_com.open_config_manual(name_port,baudrate)
            if status_open_com:
                self.open_thread_receive_and_send()
                self.com_is_open =  True
                debug_print("[1]Update thành công cổng COM")
                safe_put_queue({"type":"software","level":"info","data":"Update thành công cổng COM"})
                return True
            else:
                debug_print("[1]Update thất bại cổng COM")
                safe_put_queue({"type":"software","level":"info","data":"Update thất bại cổng COM"})
                self.com_is_open =  False
                return False
        else:
            self.close_thread_receive_and_send()
            status_open_com = self.serial_com.open_config_manual(name_port,baudrate)
            if status_open_com:
                self.open_thread_receive_and_send()
                self.com_is_open =  True
                debug_print("[2]Update thành công cổng COM")
                safe_put_queue({"type":"software","level":"info","data":"Update thành công cổng COM"})
                return True
            else:
                self.com_is_open =  False
                debug_print("[2]Update thất bại")
                safe_put_queue({"type":"software","level":"info","data":"Update thất bại cổng COM"})
                return False
            
    def send_data(self, data):
        """Đưa dữ liệu vào hàng đợi gửi"""
        try:
            self.tx_queue.put(data)
            debug_print(f"[TX Queue] ➜ {data}")
        except queue.Full:
            debug_print("⚠️ Hàng đợi gửi đầy. Không thể gửi:", data)

    def receive_data(self):
        """Nhận dữ liệu từ serial và đưa vào hàng đợi nhận"""
        data = self.serial_com.receive_data() 
        if data:
            self.send_log_erro_client(data)
            try:
                self.rx_queue.put_nowait(data)
            except queue.Full:   
                debug_print("⚠️ Hàng đợi nhận đầy serial RX  đầy. Bỏ qua dữ liệu")
                data_get_against_queue_full = self.rx_queue.get_nowait()
                debug_print("✅ Lấy ra 1 giá trị hàng đợi tránh đầy data lấy ra là: ",data_get_against_queue_full)

    def get_data_from_queue(self):   # co su dung nha
        """Lấy dữ liệu đã nhận ra khỏi hàng đợi"""
        if not self.rx_queue.empty():
            return self.rx_queue.get()
        return None
    
    def _listen_serial(self):
        safe_put_queue({"type":"software","level":"info","data":f"Mở luồng lắng nghe STM32"})
        debug_print("✅[Mở 1]:Luồng lắng nghe")
        while self.running_rx:
            try:
                self.receive_data()
                time.sleep(0.001)  # 🔑 nghỉ 1ms tránh CPU 100%
            except Exception as e:
                debug_print("[SerialListener] Lỗi:", e)
                time.sleep(2)
    def set_mode_device(self, mode):
        """Đặt chế độ thiết bị"""
        self.mode_device = mode

    def get_mode_device(self):
        """Lấy chế độ thiết bị hiện tại"""
        return self.mode_device
                
    def send_log_erro_client(self,data):
        if self.handshake_status:
            """Thực hiện điều gì đó nếu hiển thị mà không thực thi gì chỉ show lên thôi thì không cần làm gì cả 1 số log chỉ show lên cho người dùng thấy thôi"""
            if "log:PAUSE:PRESSStop" in data:
                if self.show_log != "log:PAUSE:PRESSStop":
                    shared_queue.queue_tx_web_log.put_nowait("cmd_control_log:clearn_log")
                    shared_queue.queue_tx_web_log.put_nowait("❌[ERRO] Đang dừng khẩn cấp.<br>✅Thả nút Stop và nhấn nút Reset để khởi động lại.")
            elif ("log:RELEASE_STOP" in data):
                    if self.show_log != "log:RELEASE_STOP":
                        self.show_log = "log:RELEASE_STOP"
                        shared_queue.queue_tx_web_log.put_nowait("✔️[INF] Đã thả nút stop")
                        shared_queue.queue_tx_web_log.put_nowait("✅ Nhấn nút Strart để khởi động lại.")
            elif ("log:ERROX" in data):
                if self.show_log != "erro_x":
                    shared_queue.queue_tx_web_log.put_nowait("❌[ERRO] Lỗi trục X.<br>Tắt phần mềm Reset lại máy")
                    return True
            elif ( "log:ERROY" in data):
                if self.show_log != "erro_y":
                    self.show_log = "erro_y"
                    shared_queue.queue_tx_web_log.put_nowait("\n❌[ERRO] Lỗi trục Y.\nTắt phần mềm Reset lại máy")
                    return True
            elif ( "log:ERROZ" in data):
                if self.show_log != "erro_z":
                    self.show_log = "erro_z"
                    shared_queue.queue_tx_web_log.put_nowait("\n❌[ERRO] Lỗi trục Z.\nTắt phần mềm Reset lại máy")
                    return True
            elif ( "log:PAUSED:OPENDoor" in data):
                if self.show_log != "pause_open_door":
                    self.show_log = "pause_open_door"
                    shared_queue.queue_tx_web_log.put_nowait("\n❌[WARNING] Tạm dừng máy vì đang tháo vỏ máy.\nLắp lại để hoạt động tiếp")
                    return True
            elif ( "log:PAUSED:TOUCHSafety" in data):
                if self.show_log != "log:PAUSED:TOUCHSafety":
                    self.show_log = "log:PAUSED:TOUCHSafety"
                    shared_queue.queue_tx_web_log.put_nowait("❌[WARNING] Tạm dừng vì chạm cảm biến an toàn.<br>✅Bỏ tay ra vùng cảm biến an toàn")
                    return True    
            elif ( "log:went_org" in data):
                if self.show_log != "log:went_org":
                    self.show_log = "log:went_org"
                    shared_queue.queue_tx_web_log.put_nowait("✔️[INF] Đã về gốc thành công.")
                    return True
            elif ( "log:put_new_products" in data):
                if self.show_log != "log:put_new_products":
                    self.show_log = "log:put_new_products"
                    shared_queue.queue_tx_web_log.put_nowait("cmd_control_log:clearn_log")
                    shared_queue.queue_tx_web_log.put_nowait("✔️[INF] Đã lấy sản phẩm ra.<br>✅ Đặt sản phẩm mới vào.")
                    return True
            elif ( "log:take_product_old" in data):
                    self.show_log = "log:take_product_old"
                    shared_queue.queue_tx_web_log.put_nowait("✔️[INF] Sản phẩm đã được nhận diện.<br>✅ Hãy lấy sản phẩm ra.")
                    return True     
            return False
    

    def handler_mode_auto(self):
        self.clear_tx_queue()
        self.clear_rx_queue()

    def _send_serial(self):
        debug_print("✅[Mở 2] Luồng gửi")
        safe_put_queue({"type":"software","level":"info","data":f"Mở luồng gửi STM32"})
        while self.running_tx:
            # print("luong gui dang duoc bat")
            # time.sleep(2)
            try:
                # block tối đa 0.1s để chờ data, tránh busy-wait
                data = self.tx_queue.get(timeout=0.1)
                self.serial_com.send_data(data)
            except queue.Empty:
                continue  # không có gì để gửi, quay lại vòng lặp
            except Exception as e:
                debug_print("[SerialSender] Lỗi:", e)
                time.sleep(2)

    def get_rx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi nhận"""
        size = self.rx_queue.qsize()
        debug_print(f"📥 Số lượng phần tử trong rx_queue: {size}")
        return size
    def get_tx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi gửi"""
        size = self.tx_queue.qsize()
        debug_print(f"📦 Số lượng phần tử trong tx_queue: {size}")
        return size
    def clear_rx_queue(self):
        """Xóa sạch toàn bộ hàng đợi nhận"""
        with self.rx_queue.mutex:
            size = len(self.rx_queue.queue)
            self.rx_queue.queue.clear()
        debug_print(f"🗑️ Đã xóa {size} mục trong hàng đợi nhận (clear sạch).")

    def clear_tx_queue(self):
            """Xóa sạch toàn bộ hàng đợi gửi"""
            with self.tx_queue.mutex:
                size = len(self.tx_queue.queue)
                self.tx_queue.queue.clear()
            debug_print(f"🗑️ Đã xóa {size} mục trong hàng đợi gửi (clear sạch).")
    def  get_dict_data_send_server(self):
        dict_data = self.serial_com.to_dict()
        return dict_data 
    
        
#==================================Hàm chạy kiểm thử====================================================#
# -------------------------------
# Ví dụ chạy trực tiếp
# -------------------------------
# ms = ManagerSerial(queue_tx_web_main)
# def listen_update():
#         """Luồng phụ: chờ nhấn Enter để đổi COM"""
#         while True:
#             new_port = input("Nhập cổng mới: ")
#             new_baud = int(input("Nhập baudrate mới: "))
#             ms.update_com(new_port, new_baud)
# update_thread = threading.Thread(target=listen_update, daemon=False)
# update_thread.start()

# from shared_queue import queue_tx_web_main;
# ms = ManagerSerial(queue_tx_web_main )      


































