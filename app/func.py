
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn /  Module Function utilities
# Description: Function utilities
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
from  shared_queue import queue_accept_capture,queue_tx_web_main,queue_process_capture_detect,queue_tx_web_log
from obj_log import safe_put_queue,debug_print
import threading
import time
import queue
import cv2 
TIME_OUT_WAIT_ARM_RESEND = 4
def clear_queue(q):
    """Xóa tất cả các mục trong hàng đợi."""
    while not q.empty():
        try:
            q.get_nowait()
            q.task_done()
        except queue.Empty:
            break

def wait_for_specific_data(obj_manager_serial, expected_message_1, timeout=TIME_OUT_WAIT_ARM_RESEND):
    """Hàm này chờ tín hiệu cụ thể từ obj_manager_serial.Chờ thời gian timeout giây.Sau thời gian chờ k được gửi về False.Nếu nhận đúng tín hiệu trả về True"""
    debug_print(f"⏳ Đang chờ tín hiệu:{expected_message_1} trong {timeout} giây...")
    start_time = time.time()
    expected = data_format(expected_message_1)  # chỉ xử lý 1 lần
    while time.time() - start_time < timeout:
        data = obj_manager_serial.get_data_from_queue()
        if data:
            debug_print(f"📥 PC Nhận được: {data}")
            debug_print("📥 Sau chuyển đổi :", expected)

            if data.strip() == expected:
                now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                debug_print(now_str,"✅ Nhận đúng tín hiệu mong đợi.")
                return True
            else:
                debug_print("⚠️ Tín hiệu nhận sai nội dung.")
        time.sleep(0.001)  # 🔑 tránh CPU 100% + làm chương trình mượt hơn
    debug_print(f"❌ Timeout: Không nhận được tín hiệu trong {timeout} giây.")
    return False

def is_all_int_strings(lst):
    """Hàm này dùng để kiểm tra xem tất cả phần tử trong danh sách có phải là số nguyên hợp lệ hay không."""
    try:
        return all(isinstance(int(item), int) for item in lst)
    except:
        return False
    
def data_format(arr_check):

    """Kiểm tra dữ liệu có đúng định dạng không và chuyển đổi về định dạng chuẩn.
    Ví dụ: 'cmd:1,2,3' -> 'cmd:001,002,003,ok'"""
    
    if not arr_check:
        debug_print("❌ Dữ liệu bị lỗi hoặc trống, không có dữ liệu để so sánh.")
        return False
    if arr_check.startswith("cmd:"):
        raw_data = arr_check[4:].split(",")
        raw_data = [x.strip() for x in raw_data if x.strip() != ""]

        if not raw_data:
            debug_print("❌ Không có dữ liệu tọa độ sau 'cmd:'")
            return False

        arr_covert_text = ["cmd:"]
        for i in raw_data:
            try:
                padded = f"{int(i):03}"
            except ValueError:
                debug_print(f"⚠️ Không thể chuyển '{i}' thành số nguyên.")
                return False
            arr_covert_text.append(padded)

        arr_covert_text.append("ok")
        s = ",".join(arr_covert_text[1:])
        s = "cmd:"+s
        return s
    else:
        debug_print("❌ Không phải dữ liệu tọa độ (không bắt đầu bằng 'cmd:')")
        return False
    

              
def worker_judget(queue_in,queue_out, judget_product, i, obj_arr_list_point, data_one_point_master, length,time_start):
    """Hàm luồng này  dùng để xử lý phán định sản phẩm trong đa luồng."""
    try: 
        img = queue_in.get(block=True,timeout=1)
        safe_put_queue({"type":"image","data":img}) 
        data_show_table, img_detect, is_frame_ok,arr_erro = judget_product.judget(i,
            int(obj_arr_list_point[i].z), img, data_one_point_master
        )
        data_out = {
            'index': i,
            'length': length,
            'img': img_detect,
            'data':{f"{i}":data_show_table},
            'status_frame': is_frame_ok,
            "arr_erro":arr_erro
        }
        if i == length - 1:
            data_out["total_time"] = round((time.perf_counter() - time_start) + 0.3,1)
        queue_out.put(data_out)
    except Exception as e:
        debug_print("Lỗi trong worker_judget:", e)

def process_multi_thread(queue_in, queue_out, judget_product, i, obj_arr_list_point, data_one_point_master,length,time_start):
    """Hàm này dùng để tạo luồng xử lý phán định sản phẩm trong đa luồng."""
    t = threading.Thread(
        target=worker_judget,name=f"judment_product_{i}",
        args=(queue_in, queue_out, judget_product, i, obj_arr_list_point, data_one_point_master, length,time_start),
        daemon=True 
    )
    t.start()
   
   
def run_and_capture(ID,List_point,judget_product,object_shape_master,obj_manager_serial):
    """Trả về False nếu đã cố gắng chạy nhưng không thành công trả về true nếu chạy thành công"""
    length_list_point =  len(List_point)
    data_shape_master = object_shape_master.get_quanlity_master_of_id(ID)
    if not data_shape_master:
        queue_tx_web_log.put("❌[ERRO]Chưa có dữ liệu Master. Hãy chọn \"Cấu hình master\"->\"Lấy master\"để lấy thông tin phán định.")
        return 
    time_start = time.perf_counter()
    for i in range(length_list_point):
        from_data_send_run = f"cmd:{List_point[i].x},{List_point[i].y},{List_point[i].z},{List_point[i].brightness}"
        debug_print(f"-------------------------------------Chạy lần thứ {i + 1 }-----------------------------")
        debug_print(from_data_send_run)
        debug_print(f"Phán định ID{ID} tại Index:{i}")
        data_one_point_master = object_shape_master.get_data_shape_of_location_point(ID,i)
        obj_manager_serial.send_data(from_data_send_run)
        status_send_arm = wait_for_specific_data(obj_manager_serial,from_data_send_run)
        if status_send_arm and data_one_point_master:
                queue_accept_capture.put({"training":3,"capture_detect":1})
                process_multi_thread(queue_process_capture_detect,queue_tx_web_main,judget_product,i,List_point,data_one_point_master,length_list_point,time_start)
        if not status_send_arm:
            # queue_tx_web_log.put("❌[ERRO]Đợi tín hiệu phản hồi từ ARM lỗi!")
            debug_print("❌[ERRO]Đợi tín hiệu phản hồi từ ARM lỗi!")
            debug_print("✅Chạy điểm thành Công")
        else:
            debug_print("✅Điểm điểm không thành công")
            



def frame_to_jpeg_bytes(frame, quality=90) -> bytes:
    """
    Chuyển từ numpy array (frame BGR) sang JPEG bytes.
    """
    ok, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return buffer.tobytes() if ok else None
  

def remove_vietnamese_tone(text: str) -> str:
        """Hàm này dùng để loại bỏ dấu tiếng việt trong chuỗi văn bản."""
        import unicodedata
        nfkd_form = unicodedata.normalize('NFD', text)
        without_tone = ''.join([c for c in nfkd_form if unicodedata.category(c) != 'Mn'])
        return without_tone.replace("Đ", "D").replace("đ", "d")


