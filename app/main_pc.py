
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module driver
# Description: Module driver
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
import common_value
import common_object
import shared_queue
import func
import threading
import time
from obj_log import safe_put_queue,debug_print

OPEN_TASK_MAIN_PROCESS = True
DELAY_TIME_THE_FIRST_CONNECT_COM  = 0.2
LIMIT_LEN_MIN_DATA_COM = 6

def fuc_main_process():
    from judget_product import Judget_Product
    judget_product = Judget_Product()
    from folder_create import Create
    object_folder = Create()
    while OPEN_TASK_MAIN_PROCESS:
        if common_object.obj_manager_serial.com_is_open:   #ham nay xoa
            while (common_value.the_first_connect == True):
                common_object.obj_manager_serial.set_handshake_status(False)
                common_object.obj_manager_serial.send_data("200OK:")
                common_value.status_check_connect_arm = False
                if common_object.obj_manager_serial.get_rx_queue_size() > 0:
                        data = common_object.obj_manager_serial.get_data_from_queue()
                        debug_print("Data nhận được từ Queue ARM:", data)
                        if("200OK," in data ):
                            if(len(data) <= LIMIT_LEN_MIN_DATA_COM):
                                print("❌Độ dài dữ liệu gửi về ngắn....PC Gửi lại 200OK") 
                                continue
                            cut_data = data[LIMIT_LEN_MIN_DATA_COM:].split(",")
                            debug_print("Mảng ",cut_data)
                            if cut_data == data[LIMIT_LEN_MIN_DATA_COM:]:
                                print("❌Dữ liệu không có dấu phẩy....PC Gửi lại 200OK")
                                continue
                            if (func.is_all_int_strings(cut_data) == False or len(cut_data) != 4):
                                debug_print("Dữ liệu tọa độ ban đầu không hợp lệ. Vui lòng kiểm tra lại.")
                                continue
                            if "200OK,000,000,000" in data:
                                  debug_print("........Nhan dung tin hieu dieu khien .....")
                                  common_value.the_first_connect = False
                                  common_object.obj_manager_serial.clear_rx_queue()  
                                  common_object.obj_manager_serial.clear_tx_queue()
                                  break
                            else:
                                 common_object.obj_manager_serial.send_data("cmd:0,0,0,0")
                time.sleep(DELAY_TIME_THE_FIRST_CONNECT_COM)   
            # debug_print("----------------- Bắt đầu điều khiển với ARM -------------------")
            common_object.obj_manager_serial.set_handshake_status(True)
            common_value.status_check_connect_arm =  True
            match common_value.click_page_html:
                case 6:
                    if not shared_queue.queue_rx_web_api.empty():
                        data_web_rx = shared_queue.queue_rx_web_api.get()
                        if("cmd:" in data_web_rx):
                            common_object.obj_manager_serial.clear_tx_queue()
                            common_object.obj_manager_serial.send_data(data_web_rx)
                            result_send = func.wait_for_specific_data(common_object.obj_manager_serial,data_web_rx)                   
                            if result_send:
                                shared_queue.queue_tx_web_log.put(f"\n✔️Chạy {data_web_rx} thành công")
                            else :
                                shared_queue.queue_tx_web_log.put(f"\n❌Chạy {data_web_rx} thất bại")    
                case 1:
                    # debug_print("--- Đang ở trang phán định----")
                    if(common_value.is_run == 1 and common_object.obj_manager_serial.get_data_from_queue() == "ready")   : 
                        if common_value.status_check_connect_arm  and common_value.status_check_connect_camera :
                            object_folder.create_choose_master(common_value.NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
                            choose_master_index = object_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
                            choose_master_index =  choose_master_index.strip()                 
                            if "0" == choose_master_index:
                                    shared_queue.queue_tx_web_log.put("❌Bạn chưa chọn loại sản phẩm. Cần \"Chọn loại sản phẩm\" trước khi nhấn \"Chạy\"!")
                                    shared_queue.queue_tx_web_log.put("❌Hoặc sản phẩm chưa được tạo. Cần \"Thêm sản phẩm mới\"")
                                    continue
                            arr_point = common_object.manage_product.get_list_point_find_id(choose_master_index)
                            if arr_point:
                                    common_object.obj_manager_serial.clear_rx_queue()
                                    common_object.obj_manager_serial.clear_tx_queue()
                                    func.run_and_capture(choose_master_index,arr_point,judget_product,common_object.shape_master,common_object.obj_manager_serial)
                            elif isinstance(arr_point,list):
                                if len(arr_point)==0:
                                    shared_queue.queue_tx_web_log.put("❌Bạn chưa lấy Master cho điểm nào. Hãy vào \"Cấu hình master->Chỉnh sửa master->Thêm master\" để cấu hình cho sản phẩm")
                            else:
                                debug_print("Hiên tại các điểm đang bị rỗng")
                                shared_queue.queue_tx_web_log.put("❌Sản phẩm không tồn tại. Hãy \"Thêm sản phẩm mới\"->\"Chọn loại sản phẩm\"->\"Cấu hình master\"")
                        else:
                             if not common_value.status_check_connect_arm: 
                                   shared_queue.queue_tx_web_log.put("\n❌Hiện tại COM chưa kết nối chưa thể chạy")
                             if not common_value.status_check_connect_camera: 
                                   shared_queue.queue_tx_web_log.put("\n❌Hiện tại Camera chưa kết nối chưa thể chạy")
                             continue
                                  
            time.sleep(0.1)
        else:
            common_value.status_check_connect_arm = False
            common_value.the_first_connect = True
            time.sleep(1)
            debug_print("❌ Không tìm thấy cổng Serial. Vui lòng kiểm tra kết nối.")
            
main_process = threading.Thread(target=fuc_main_process,name="main_pc",daemon=True)
main_process.start()     
    