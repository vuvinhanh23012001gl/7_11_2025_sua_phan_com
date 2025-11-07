
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module request API client
# Description: API request clinet
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------

from flask import Blueprint,render_template,request,jsonify,send_file
import common_object
from datetime import datetime
import webbrowser
import shared_queue
import common_value 
import time
import func
import os

# Đăng ký Blueprint    

main_html = Blueprint("main",__name__)
api = Blueprint("api",__name__)
api_choose_master = Blueprint("api_choose_master",__name__)
api_take_master = Blueprint("api_take_master",__name__)
api_run_application = Blueprint("api_run_application",__name__)
api_new_product = Blueprint("api_new_product",__name__)
api_add_master = Blueprint("api_add_master",__name__)
api_config_camera = Blueprint("api_config_camera",__name__)
api_config_com = Blueprint("api_config_com",__name__)
api_config_software = Blueprint("api_config_software",__name__)
api_inf_software = Blueprint("api_inf_software",__name__)
api_login_software =  Blueprint("api_login_software",__name__)
api_reset_count_product = Blueprint("api_reset_count_product",__name__)
api_out_app = Blueprint("api_out_app",__name__)

# open website automatic
def open_browser():
    """Hàm này dùng để tự động bật web sau khi mở phần mềm """
    safe_put_queue({"type":"software","level":"info","data":f"gọi http://127.0.0.1:5000 mở trình duyệt"})
    webbrowser.open("http://127.0.0.1:5000", new=2)  # new =2 mở tab mới nếu có thể


# -----------------------Task-----------------------------------------------
def stream_frames():
    """Hàm này dùng để kiểm tra và bật luồng khởi động Camera"""
    safe_put_queue({"type":"software","level":"info","data":f"Camera chưa được mở"})
    while OPEN_THREAD_STREAM:
         common_object.cam_basler.run_cam_html()
         time.sleep(1)
    common_object.cam_basler.release()
    debug_print("Thoát luồng gửi video thành công")

# -----------------------Task-----------------------------------------------
def stream_img():
    """Hàm này dùng để gửi ảnh và dữ liệu sau khi xử lý lên web"""
    global OPEN_THREAD_IMG
    arr_save_status_frame_ok = []
    arr_erro = []
    while OPEN_THREAD_IMG:
        if shared_queue.queue_tx_web_main.qsize() > 0:
            data_img_detect = shared_queue.queue_tx_web_main.get(block=False)
            img = data_img_detect.get("img",None)
            status_open_log_excell = common_object.obj_manager_log.get_open_log_excell()
            try:
                img_convert  = func.frame_to_jpeg_bytes(img)
                data_img_detect["img"] = img_convert
                index = data_img_detect.get("index",-1)
                length = data_img_detect.get("length",-1)
                status_frame = data_img_detect.get("status_frame",-1)
                if status_open_log_excell:
                    erro_log_excell = data_img_detect.get("arr_erro",-1)
                    if (erro_log_excell !=-1):
                        if isinstance(erro_log_excell,list):
                            if erro_log_excell:
                                arr_erro.append(erro_log_excell)
                if status_frame != -1 and index >= 0:
                    arr_save_status_frame_ok.append(status_frame)
                if index!=-1 and length != -1:
                    if index == length -1 :
                        status_judment =  all(arr_save_status_frame_ok)
                        if status_judment : 
                            common_object.obj_count.increase_ok()
                            from_data_send_run = f"cmd:0,0,0,0"
                            common_object.obj_manager_serial.send_data(from_data_send_run)
                        else:
                            common_object.obj_count.increase_ng()
                        product_ok,product_ng = common_object.obj_count.read_data()
                        data_img_detect["total_product_ok"] = product_ok
                        data_img_detect["total_product_ng"] = product_ng
                        data_img_detect["status_judment"] = status_judment
                        arr_save_status_frame_ok = []
                        data_user_login = common_object.obj_manage_user.get_current_account()
                        if data_user_login and status_open_log_excell:
                            type = data_user_login.get("type","None")
                            first_name = data_user_login.get("first_name","admin")
                            last_name = data_user_login.get("last_name","admin")
                            user_name = data_user_login.get("user_name","admin")
                            line = data_user_login.get("line","None")
                            usine = data_user_login.get("usine","None")
                            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            safe_put_queue({"type":"excel","data":[now_str,f"{first_name} {last_name}",user_name,type,usine,line,"OK" if status_judment else "NG"," ".join(t.strip() for s in arr_erro for t in s) if arr_erro else ""]})
                        arr_erro= []
                common_object.socketio.emit("photo_taken",data_img_detect, namespace="/img_and_data")
            except:
                debug_print("convert anh khong thong cong")
        time.sleep(0.001)

# -----------------------Task-----------------------------------------------
def stream_logs():
    """Hàm này dùng để gửi log trạng thái phần mềm lên web"""
    while OPEN_THREAD_LOG:  
            common_value.status_check_connect_camera = common_object.cam_basler.is_camera_stable()
            common_object.socketio.emit("status_connect_com_arm", {"status":common_value.status_check_connect_arm}, namespace='/log')
            common_object.socketio.emit("status_connect_camera", {"status":common_value.status_check_connect_camera}, namespace='/log')   
            match common_value.click_page_html:
                case 3:
                    if not shared_queue.queue_tx_web_log.empty():
                        common_object.socketio.emit("log_take_master", {"log": f"{shared_queue.queue_tx_web_log.get()}"}, namespace='/log')
                case 4:
                    log_message = common_object.manage_product.get_all_ids_and_names()      # Gửi log cho thêm sản phẩm mới
                    if log_message:
                        common_object.socketio.emit("log_message", {"log_create_product": log_message}, namespace='/log')
                case 6:
                    if not shared_queue.queue_tx_web_log.empty():
                        common_object.socketio.emit("log_data", {"log": f"{shared_queue.queue_tx_web_log.get()}"}, namespace='/log')
                case 2:
                    if not shared_queue.queue_tx_web_log.empty():
                        common_object.socketio.emit("log_message", {"log_training": f"{shared_queue.queue_tx_web_log.get()}"}, namespace='/log')    #Gửi log cho File Training
                case 1: # main
                    # queue_tx_web_log.put("xin chao ban")
                    if not shared_queue.queue_tx_web_log.empty():
                        common_object.socketio.emit("log_message_judment", {"log_data": f"{shared_queue.queue_tx_web_log.get()}"}, namespace='/log')
            # debug_print(common_value.click_page_html)
            time.sleep(0.2)
# -----------------------End Task-----------------------------------------------



# socketio connect
@common_object.socketio.on('connect', namespace='/video')
def video_connect():
    """socketio connect /video"""
    debug_print("Client connected to /video")

@common_object.socketio.on('connect', namespace='/img_and_data')
def handle_video_connect():
    """socketio connect /img_and_data"""
    debug_print("📡 Client connected to /img_and_data")

@common_object.socketio.on('connect', namespace='/log')
def handle_log_connect():
    """socketio connect /log"""
    debug_print("📡 Client connected to /log")

@common_object.socketio.on('connect',namespace='/data_add_master')  #'/data_add_master' img + loction point,...
def handle_data_send_connect():
    """socketio connect /data_add_master"""
    debug_print("📡 Client connect to /data_add_master") #img hiển thị hình ảnh sản phẩm

# ----------------------------------------------Blueprint main-------------------------------

@main_html.route("/empty_page.html")
def already_open():
    # Đây là trang báo lỗi khi user mở tab thứ 2
    """Là hàm hiển thị trang báo lỗi khi mở tab thứ 2"""
    safe_put_queue({"type":"software","level":"warning","data":"Người dùng nhấn 2 trang HTML."})
    return render_template("empty_page.html")

@main_html.route("/")
def show_main():
    """Là hàm hiển thị giao diện chính trên Html"""
    obj_create_folder.create_choose_master(common_value.NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)#đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    name_product = common_object.manage_product.get_product_name_find_id(choose_master_index.strip())
    arr_type_id = common_object.manage_product.get_list_id_product()
    common_value.click_page_html = 1  # thong bao dang o trang web chinh
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        debug_print(f"gui data master co ten {choose_master_index}")
        path_arr_img = common_object.manage_product.get_list_path_master_product_img_name(data_strip)
        product_ok,product_ng = common_object.obj_count.read_data()
        return render_template("show_main.html",path_arr_img = path_arr_img,product_ok = product_ok,product_ng = product_ng,name_product = name_product)
    return render_template("show_main.html",path_arr_img = None,product_ok = 0,product_ng = 0,name_product="")

#--------------------------------------------------------Api_run_application---------------------------------------------
@api_run_application.route('/run_application',methods = ['GET'])
def run_application():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút Run application"""
    debug_print("Đã nhấn nút Run application")
    common_value.is_run = 1
    return jsonify({"status":"OK"})


#--------------------------------------------------------Api_master_take---------------------------------------------

@api_take_master.route("/master_close",methods=["POST"])
def master_close():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang take master"""
    common_value.click_page_html = 1  #Ve lai main chinh
    data = request.get_json()
    debug_print(data)
    return jsonify({'status':"OKE"})


@api_take_master.route("/master_take",methods=["POST"])  #Khi nhan vao take masster thi thuc hien gui anh len truoc
def master_take():
    """Hàm này khi người dùng vào trang take master thì gửi ảnh master và dữ liệu shape lên web"""
    safe_put_queue({"type":"software","level":"info","data":"KTV đã truy cập vào lấy master"})
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    common_value.click_page_html = 3  
    data = request.get_json()
    debug_print(data)
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = common_object.manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        debug_print(f"gui data master co ten {choose_master_index}")
        path_arr_img = common_object.manage_product.get_list_path_master_product_img_name(data_strip)
        debug_print("path_arr_img",path_arr_img)
        common_object.shape_master.load_file()
        debug_print("\nshape_master.get_data_is_id(data_strip) la:------------------------\n",common_object.shape_master.get_data_is_id(data_strip))
        return {"path_arr_img": path_arr_img,"Shapes":common_object.shape_master.get_data_is_id(data_strip)}
    return {"path_arr_img": None,"Shapes":None}


@api_take_master.route("/config_master",methods=["POST"])
def config_master():
    """Hàm này dùng để nhận dữ liệu shape từ web khi người dùng nhấn nút Lưu cấu hình master"""
    data = request.get_json()
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    choose_master_index = str(choose_master_index).strip()
    status_check = common_object.shape_master.check_all_rules(data)
    if status_check:
        status_save = common_object.shape_master.save_shapes_to_json(choose_master_index,data)
        if status_save:
            common_object.shape_master.load_file()
            shared_queue.queue_tx_web_log.put_nowait("[Server]Lưu dữ liệu thành công")
            safe_put_queue({"type":"software","level":"info","data":"KTV [Server]Lưu dữ liệu thành công"})
        else:
            shared_queue.queue_tx_web_log.put_nowait("[Server]Lưu dữ liệu thất bại")
            safe_put_queue({"type":"software","level":"info","data":"KTV [Server]Lưu dữ liệu thất bại"})
    else:
        debug_print("Dữ liệu bị lỗi")
        shared_queue.queue_tx_web_log.put_nowait("[Server]Kiểm tra dữ liệu bị sai")
        safe_put_queue({"type":"software","level":"error","data":"Kiểm tra dữ liệu lấy master bị sai"})
    return jsonify({'status':"OKE"})



#--------------------------------------------------------Api_new_product ---------------------------------------------

@api_new_product.route("/add")
def add():
     """Hàm này dùng để hiển thị trang thêm sản phẩm mới khi người dùng nhấn nút Thêm sản phẩm mới"""
     safe_put_queue({"type":"software","level":"info","data":"KTV đã nhấn vào thêm sản phẩm mới."})
     common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
     common_value.click_page_html = 4
     return render_template("save_product_new.html")

@api_new_product.route("/upload", methods=["POST"])
def upload_product():
    """Hàm này dùng để nhận dữ liệu từ web khi người dùng nhấn nút Lưu sản phẩm mới"""
    # ---- Lấy dữ liệu text từ form ----
    product_id = request.form.get("product_id")
    product_name = request.form.get("product_name")
    limit_x = request.form.get("limit_x")
    limit_y = request.form.get("limit_y")
    limit_z = request.form.get("limit_z")
    description = request.form.get("description")
    # ---- Lấy file từ form ----
    file = request.files.get("file_upload")
    try:
        product_id = str(product_id)
        product_name = str(product_name)
        limit_x = int(limit_x.strip())
        limit_y = int(limit_y.strip())
        limit_z = int(limit_z.strip())
    except:
        debug_print("Dữ liệu gưi về lỗi")
        safe_put_queue({"type":"software","level":"warning","data":"KTV thêm sản phẩm mới dữ liệu gửi về lỗi"})
        return jsonify({"success": False, "ErrorDataIncorect": "Dữ liệu bị gửi sai"}), 400
    if not file:
        debug_print("Chưa nhận được File ảnh sản phẩm")
        safe_put_queue({"type":"software","level":"warning","data":"KTV chưa thêm file ảnh"})
        return jsonify({"success": False, "ErrorNotSendFile": "Hãy chọn hình ảnh sản phẩm"}), 400

    # ---- Thư mục và tên file muốn lưu ----
    status_create_manage = common_object.manage_product.add_product_type(product_id,product_name,[limit_x,limit_y,limit_z],description)
    debug_print("status_create_manage la:............",status_create_manage)
    if not status_create_manage:
        debug_print("Sản phẩm loại này đã tồn tại .Hãy đặt ID khác hoặc tìm sản phẩm trong danh sách sản phẩm")
        return jsonify({"success": False, "ErroHasExitsed": "Sản phẩm loại này đã tồn tại .Hãy đặt ID khác hoặc tìm sản phẩm trong danh sách sản phẩm"}), 400
    save_dir = common_object.manage_product.absolute_path(product_id)
    if not save_dir:
        debug_print("Tìm không ra sản link ảnh sản phẩm vừa tạo ra")
        return jsonify({"success": False, "ErroNotFileImg": "Tìm không ra sản link ảnh sản phẩm vừa tạo ra"}), 400
    debug_print("Đường dẫn tới ảnh",save_dir)
    save_filename = f"Img_{product_id}.png"     # tên file mong muốn
    debug_print("Tên ảnh lưu là",save_filename)
    save_path = os.path.join(save_dir, save_filename)
    # ---- Lưu file ----
    file.save(save_path)
    # ---- Trả kết quả về client ----
    safe_put_queue({"type":"software","level":"info","data":"KTV Sản phẩm mới đã được thêm"})

    return jsonify({
        "success": True,
        "product_id": product_id,
        "product_name": product_name,
        "limit_x": limit_x,
        "limit_y": limit_y,
        "limit_z": limit_z,
        "saved_path": save_path,                       # đường dẫn trên server
        "url": f"/static/Product_Photo/{save_filename}"  # đường dẫn để truy cập từ browser
    })
#--------------------------------------------------------Api_choose_master---------------------------------------------

@api_choose_master.route("/get_show_main",methods = ["POST"])
def get_content():
    """Hàm này dùng để nhận chọn sản phẩm khi người dùng nhấn nút Chọn sản phẩm và trả về trang show_main chính"""
    json_data = request.get_json()
    choose_master = json_data.get('data')
    debug_print(f"Master được chọn là : {choose_master}")
    safe_put_queue({"type":"software","level":"info","data":f"Master được chọn là : {choose_master}"})
    obj_create_folder.clear_file_content(common_value.NAME_FILE_CHOOSE_MASTER)
    obj_create_folder.write_data_to_file_in_folder_static(common_value.NAME_FILE_CHOOSE_MASTER,choose_master)
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_choose_master.route("/chose_product")
def chose_product():
    """Hàm này trả về trang chọn sản phẩm khi người dùng nhấn nút Chọn sản phẩm"""
    common_object.cam_basler.disable_send_video() # ngan nguoi dung nhan linh tinh khi dang gui video len nha
    common_value.click_page_html = 5
    data =  common_object.manage_product.get_file_data() 
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)
    debug_print("Data gui len server ",data)
    return render_template("chose_product.html",data = data,choose_master = choose_master_index)

@api_choose_master.route("/exit")
def exit_choose_master():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang chọn sản phẩm"""
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)
@api_choose_master.route("/erase_product",methods = ["POST"]) #phan nay co ban la oke1 roi 
def erase_product():
    """Hàm này dùng để nhận lệnh xóa sản phẩm khi người dùng nhấn nút Xóa sản phẩm"""
    debug_print("------------------------------------------Tiến hành xóa bắt đầu----------------------------------")
    data = request.get_json()
    debug_print(data)
    Choose_product_erase = data.get("Choose_product_erase",-1)
    debug_print(Choose_product_erase)
    if Choose_product_erase != -1 :
        status_erase_product = common_object.manage_product.remove_product_type(Choose_product_erase,common_object.shape_master)
        if status_erase_product:
            common_object.shape_master.load_file()
            response = {
                'redirect_url':'/'
            }
            debug_print("------------------------------------------Xoa thanh cong master----------------------------------")
            return jsonify(response)

        else :
            debug_print("------------------------------------------Tiến hành xóa kết thúc 2----------------------------------")
            return jsonify({"status":"200OK","erase":"NG"})
    else:
        debug_print("------------------------------------------Tiến hành xóa kết thúc 3----------------------------------")
        debug_print("Không nhận được data chuẩn Form")
    safe_put_queue({"type":"software","level":"info","data":f"KTV đã xóa sản phẩm"})
    return jsonify({"status":"200OK","erase":None})


#----------------------------------------------api_add_master------------------------------------------------------
@api_add_master.route("/run_point",methods=['POST'])
def run_point():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút Run point"""
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    brightness = data.get('brightness')
    data_send = f"cmd:{x},{y},{z},{brightness}"
    debug_print(f'x ={x}, y = {y}, z = {z} brightness ={brightness}')
    shared_queue.queue_rx_web_api.put(data_send)  # //Can than Request nhieu de bi day
    return jsonify({"message": "Ok"})

@api_add_master.route("/run_all_master",methods=["POST"],strict_slashes=False)
def run_all_master():
    """Hàm này dùng để nhận lệnh từ web khi người dùng nhấn nút Run all master"""
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = common_object.manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        arr_point = common_object.manage_product.return_data_list_point(data_strip)
        debug_print("arr_point",arr_point)
        debug_print("len arr_point",len(arr_point))
        if arr_point:
            for point in arr_point:
                   x=point.get("x",-1)
                   y=point.get("y",-1)
                   z=point.get("z",-1)
                   brightness=point.get("brightness",-1)
                   if x == -1 or y == -1 or z==-1 or brightness==-1:
                       return jsonify({"status_run":"erro"})
                   else :
                       data_send = f"cmd:{x},{y},{z},{brightness}"
                   debug_print(data_send)
                   shared_queue.queue_rx_web_api.put(data_send)
            return jsonify({"status_run":"oke"})
        else:
            debug_print("Không tìm thấy ID ")
            return jsonify({"status_run":"erro"})
    else:
        return jsonify({"status_run":"erro"})


@api_add_master.route("/exit")
def exit_add_master():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang thêm master"""
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nhan thoat
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_add_master.route("/",methods=["POST"],strict_slashes=False)
def api_add_master_tree():
    """Hàm này dùng để nhận lệnh từ web bắt đầu vẽ shape trên master """
    common_value.click_page_html = 6  #Ve lai main chinh
    data = request.get_json()
    debug_print(data)
    choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = common_object.manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    common_object.cam_basler.enable_send_video()
    if data_strip in  arr_type_id:
        debug_print(f"gui data master co ten {choose_master_index}")
        path_arr_img = common_object.manage_product.get_list_path_master_product_img_name(data_strip)
        arr_point = common_object.manage_product.return_data_list_point(data_strip)
        debug_print(path_arr_img)
        inf_product = common_object.manage_product.get_all_ids_and_names()
        common_object.socketio.emit("data_realtime", {
            "path_arr_img": path_arr_img,
            "arr_point": arr_point,
            "inf_product": inf_product
        },namespace='/data_add_master')
        return {"path_arr_img": path_arr_img,"arr_point":arr_point,"inf_product":inf_product}
    return {"path_arr_img": None,"arr_point":None,"inf_product":None}

@api_add_master.route("/erase_index",methods=["POST"],strict_slashes=False)
def erase_index():
    """Hàm này để xóa master thứ index"""
    safe_put_queue({"type":"software","level":"info","data":f"KTV đã xóa ảnh master thứ index"})
    data  =  request.get_json()
    choose_id = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    choose_id_strip = choose_id.strip()
    index = data.get("index",-1)
    if index != -1:
        debug_print("choose_id_strip",choose_id_strip)
        debug_print("index :",index)
        common_object.manage_product.remove_all_master_index(str(choose_id_strip),int(index),common_object.shape_master)
        path_arr_img = common_object.manage_product.get_list_path_master_product_img_name(choose_id_strip)
        arr_point = common_object.manage_product.return_data_list_point(choose_id_strip)
        # print(path_arr_img)
        for value1, value2 in zip(path_arr_img, arr_point):
            debug_print("path:",value1)
            debug_print("point:",value2)
        debug_print("du lieu master sau khi xoa xem de biet cap nhat thong cong hay chua",common_object.shape_master.get_data_is_id(choose_id_strip))
        inf_product = common_object.manage_product.get_all_ids_and_names()
        common_object.socketio.emit("data_realtime", {
                            "path_arr_img": path_arr_img,
                            "arr_point": arr_point,
                            "inf_product": inf_product
                    },namespace='/data_add_master')
    return jsonify({"message":"OK"})


@api_add_master.route("/capture_master",methods=["POST"],strict_slashes=False)
def capture_master():
       """Hàm này dùng để nhận dữ liệu từ web khi người dùng nhấn nút Chụp ảnh master"""

       #néu có ảnh sẵn rồi thì không tạo file nữa và chỉnh sửa điểm trong index nếu chua có điểm thì đó là sản phẩm mới thì sẽ tạo ra file mới ảnh mới , thêm điẻm mới
       data = request.get_json()
       index_capture = data.get("index",-1)
       x = data.get("x",-1)
       y = data.get("y",-1)
       z = data.get("z",-1)
       k = data.get("k",-1)

       debug_print("type",type(x),type(y))
       choose_master_index = obj_create_folder.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
       arr_type_id = common_object.manage_product.get_list_id_product()
       data_strip = choose_master_index.strip()
       if data_strip in  arr_type_id:
            status_camera = common_object.cam_basler.is_camera_stable()
            if status_camera :
                status = common_object.manage_product.create_file_and_path_img_master(data_strip,f"img_{index_capture}.png")
                debug_print(status)
                if status:
                    status_create_file = status.get("return",-1)
                    path = status.get("path",-1)
                    if status_create_file != -1 and path!=-1 and status_create_file == True:
                        debug_print("Tiến hành lưu ảnh mới điểm mới...")
                        debug_print("xyz",x,y,z,k,index_capture)
                        shared_queue.queue_accept_capture.put_nowait({"training":3,"name_capture":path})
                        common_object.manage_product.add_list_point_to_product(data_strip,int(x.strip()),int(y.strip()),int(z.strip()),int(k.strip()))
                    elif (status_create_file != -1 and path!=-1 and status_create_file == False):
                        debug_print("Tiến hành sửa điểm cũ lưu ảnh mới...")
                        debug_print("xyz",x,y,z,k,index_capture)
                        shared_queue.queue_accept_capture.put_nowait({"training":3,"name_capture":path})
                        common_object.manage_product.fix_score_point_product(data_strip,int(x.strip()),int(y.strip()),int(z.strip()),int(k.strip()),index_capture)
                    else:
                        debug_print("Tạo File thất bại")
                    path_arr_img = common_object.manage_product.get_list_path_master_product_img_name(data_strip)
                    arr_point = common_object.manage_product.return_data_list_point(data_strip)
                    debug_print(path_arr_img)
                    inf_product = common_object.manage_product.get_all_ids_and_names()
                    common_object.socketio.emit("data_realtime", {
                            "path_arr_img": path_arr_img,
                            "arr_point": arr_point,
                            "inf_product": inf_product
                    },namespace='/data_add_master')
                else:
                    debug_print("Tạo File thất bại")
                    shared_queue.queue_tx_web_log.put_nowait("\nThêm thất bại")
            else:
                shared_queue.queue_tx_web_log.put_nowait("Camera hiện tại không hoạt động nên không thể chụp ảnh được\n")
                debug_print("Camera hiện tại không hoạt động nên không thể chụp ảnh được")
       else:
           debug_print("Không tìm thấy sản phẩm có ID trong danh sách ID đã lưu để chụp ảnh\n")
       return jsonify({'status':"200OK"})

#----------------------------------------------------api_config_camera-------------------------------------------
@api_config_camera.route("/exit")
def exit_api_config_camera():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang cấu hình camera"""
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_config_camera.route("/get_data_show",strict_slashes=False)
def get_data_show():
    """Hàm này dùng để gửi dữ liệu cấu hình camera lên web khi người dùng vào trang cấu hình camera"""
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    common_value.click_page_html = 8 # Câu hình cổng com
    data_show = common_object.cam_basler.show_file_config()
    return jsonify({"status":"200OK","data":data_show})

#----------------------------------------------------api_config_software-------------------------------------------
@api_config_software.route("/exit")
def exit_api_config_software():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang cấu hình phần mềm"""
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)



@api_config_software.route("/config_software",strict_slashes=False)
def config_software():
    """Hàm này dùng để gửi dữ liệu cấu hình phần mềm lên web khi người dùng vào trang cấu hình phần mềm"""
    safe_put_queue({"type":"software","level":"info","data":f"KTV đã vào configsoftware"})
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    data_send_client = common_object.obj_config_software.to_dict()
    return jsonify({"status":"200OK","data":data_send_client})


@api_config_software.route("/change_log",methods=["POST"],strict_slashes=False)
def change_log(): 
    """Hàm này dùng để nhận dữ liệu từ web khi người dùng thay đổi cấu hình log phần mềm"""  
    data_change = request.get_json()
    status_log_img = data_change.get("log_img",True)
    status_log_product = data_change.get("log_product",True)
    status_log_software = data_change.get("log_software",True)
    status_log_console = data_change.get("log_console",True)
    set_time_save_log_software = data_change.get("set_time_save_log_software",30)
    set_time_save_log_img = data_change.get("set_time_save_log_img",30)
    set_time_save_log_excell = data_change.get("set_time_save_log_excell",30)
    common_object.obj_config_software.update_open_btn(
        status_log_img,status_log_product,status_log_software,status_log_console,
        int(set_time_save_log_software),int(set_time_save_log_img),int(set_time_save_log_excell)
    )
    common_object.obj_manager_log.update_log()
    # common_object.obj_log.info(f"Update trạng thái các nút nhấn btn_IMG:{status_log_img} btn_excell:{status_log_product} btn_log_txt:{status_log_software}")
    return jsonify({"status":"Cấu hình thành công!"})


#----------------------------------------------------api_config_com-------------------------------------------
@api_config_com.route("/exit")
def exit_api_config_com():
    """Hàm này dùng để nhận lệnh từ web khi nhấn nút thoát trang cấu hình cổng com"""
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_config_com.route("/get_list_com",strict_slashes=False)
def get_list_com():
    """Hàm này dùng để gửi danh sách cổng com lên web khi người dùng vào trang cấu hình cổng com"""
    common_value.click_page_html = 7 # Câu hình cổng com
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    arr_com = common_object.obj_manager_serial.serial_com.show_list_port()
    data_connect = common_object.obj_manager_serial.get_dict_data_send_server()
    return jsonify({"status":"200OK","data":arr_com,"data_connected":data_connect})

@api_config_com.route("/open_and_save_inf",methods=["POST"],strict_slashes=False)
def open_and_save_inf():
    """Hàm này dùng để nhận dữ liệu từ web khi người dùng nhấn nút Mở cổng com và Lưu cấu hình cổng com"""
    data = request.get_json()
    com_choose = data.get("com_choose",-1)
    baudrate_choose = data.get("baudrate_choose", -1)
    if baudrate_choose == -1 or com_choose == -1:
        debug_print("Lỗi nhận dũ liệu")
        return jsonify({"error": "Không dữ liệu không hợp lệ"}), 400
    if not data:
        return jsonify({"error": "Không trống dữ liệu"}), 400
    com_choose = str(com_choose).strip()
    baudrate_choose = int(baudrate_choose)
    debug_print("com_choose",com_choose,"baudrate_choose",baudrate_choose)
    status_config =  common_object.obj_manager_serial.update_com(com_choose,baudrate_choose)
    if status_config:
        debug_print("Đổi cổng thành công nha !!!!!!!!")
        common_value.the_first_connect = True  # bat dau  reset lai gui 200 OK
        data_connect = common_object.obj_manager_serial.get_dict_data_send_server()
        return jsonify({"status":"200OK","data":data_connect})
    else:
        return jsonify({"error": "Lỗi không mở được cổng com"}), 400



#----------------------------------------------------api_inf_software-------------------------------------------
@api_inf_software.route("/download_manual")
def download_manual():
    """Hàm này dùng để tải file hướng dẫn sử dụng phần mềm"""
    debug_print("Trả File Hướng dẫn sử dụng sản phẩm cho clinet")
    return send_file("static/docurment_manual/HuongDan.pdf", mimetype="application/pdf")

@api_inf_software.route("/data_infor_software") #thong tin phan mem 
def data_infor_software():
    """Hàm này dùng để gửi thông tin phần mềm lên web khi người dùng vào trang thông tin phần mềm"""
    common_object.cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    data_send_client = common_object.obj_config_software.to_dict_infor_software()
    debug_print("Trả thông tin phần mềm cho clinet")
    return jsonify({"status":"200OK","data":data_send_client})


#----------------------------------------------------api_login_software-------------------------------------------
@api_login_software.route("/login",methods=["POST"])
def login():
    """Hàm này dùng để nhận dữ liệu từ web khi người dùng nhấn nút Đăng nhập"""
    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()
    debug_print("username","password",username,password)
    is_user,type_user = common_object.obj_manage_user.check_account(username,password)
    if is_user:
         return jsonify({"success": True,"type":type_user,"message": "Đăng nhập thành công"})   # type == True la admin nguoc lai la user
    else:
        return jsonify({"success": False,"message": "Sai tài khoản hoặc mật khẩu"})
    
@api_login_software.route("/register_an_account",methods=["POST"])
def register_an_account():
    """Hàm này dùng để nhận dữ liệu từ web khi người dùng nhấn nút Đăng kí tài khoản"""
    data = request.get_json()
    debug_print(data)
    debug_print("Bạn vừa nhấn vào nút đăng kí tài khoản")
    first_name = data.get("first_name",None)
    last_name = data.get("last_name",None)
    factory = data.get("factory",None)
    line = data.get("line",None)
    user = data.get("user",None)
    password = data.get("pass",None)
    if not all([first_name, last_name, factory, line, user, password]):
        return jsonify({"success": False,"message": "Đăng kí thất bại"})   # typ
    first_name = first_name.strip()
    last_name = last_name.strip()
    factory = factory.strip()
    line = line.strip()
    user = user.strip()
    password = password.strip()
    status_register_an_account,status_erro = common_object.obj_manage_user.create_user(user,password,first_name,last_name,line,factory)

    if status_register_an_account:
        safe_put_queue({"type":"software","level":"info","data":"Đăng kí tài khoản thành công"})
        return jsonify({"success": True,"message": status_erro})  
     
    else:
        safe_put_queue({"type":"software","level":"info","data":"Đăng kí tài khoản thất bại"})
        return jsonify({"success": False,"message": status_erro})  

#----------------------------------------------------api_reset_count_product-------------------------------------------
@api_reset_count_product.route("/click_reset",methods=["POST"])
def click_reset():
    """Hàm này dùng để nhận lệnh từ web khi người dùng nhấn nút Reset count sản phẩm"""
    safe_put_queue({"type":"software","level":"info","data":"Người dùng nhấn reset sản phẩm trên truyền"})
    common_object.obj_count.reset() 
    return jsonify({'status':"OK"})


#----------------------------------------------------api_out_app-------------------------------------------
@api_out_app.route("/process_out_app",methods=["POST"])
def process_out_app():
        """Hàm này dùng để nhận lệnh từ web khi người dùng nhấn nút thoát phần mềm"""
        safe_put_queue({"type":"software","level":"info","data":"Người dùng nhấn thoát phần mềm"})
        time.sleep(0.5)
        global OPEN_THREAD_LOG,OPEN_THREAD_STREAM,OPEN_THREAD_IMG
        debug_print("Người dùng đã nhấn nút thoát phần mềm")
        debug_print("Tiến hành thoát app...")
        common_object.obj_manager_serial.close_thread_receive_and_send()
        common_object.cam_basler.stop_emit_loop()
        common_object.obj_manager_log.stop_log_thread()
        OPEN_THREAD_LOG =  False
        OPEN_THREAD_STREAM =  False
        OPEN_THREAD_IMG = False
        main_pc.OPEN_TASK_MAIN_PROCESS = False
        debug_print("Đã tắt hết các tiến trình con...")
        os._exit(0)
        return jsonify({'status':"OK"})

#--------------------------------------------------------End Api----------------------------------------------

common_object.app.register_blueprint(main_html)
common_object.app.register_blueprint(api, url_prefix="/api")
common_object.app.register_blueprint(api_choose_master, url_prefix="/api_choose_master")
common_object.app.register_blueprint(api_take_master, url_prefix="/api_take_master")
common_object.app.register_blueprint(api_run_application, url_prefix="/api_run_application")
common_object.app.register_blueprint(api_new_product, url_prefix="/api_new_product")
common_object.app.register_blueprint(api_add_master, url_prefix="/api_add_master")
common_object.app.register_blueprint(api_config_camera, url_prefix="/api_config_camera")
common_object.app.register_blueprint(api_config_com, url_prefix="/api_config_com")
common_object.app.register_blueprint(api_config_software, url_prefix="/api_config_software")
common_object.app.register_blueprint(api_inf_software, url_prefix="/api_inf_software")
common_object.app.register_blueprint(api_login_software, url_prefix="/api_login_software")
common_object.app.register_blueprint(api_reset_count_product, url_prefix="/api_reset_count_product")
common_object.app.register_blueprint(api_out_app, url_prefix="/api_out_app")


if __name__ == "__main__":
    
    OPEN_THREAD_LOG =  True
    OPEN_THREAD_STREAM =  True
    OPEN_THREAD_IMG = True
    from obj_log import safe_put_queue,debug_print
    import main_pc
    main_pc.OPEN_TASK_MAIN_PROCESS = True
    from folder_create import Create
    obj_create_folder = Create()
    import threading
    threading.Thread(target=stream_logs,name="stream_log",daemon = True).start()
    threading.Thread(target=stream_img,name="stream_img_and_data",daemon = True).start()
    threading.Thread(target = stream_frames,name="stream_video",daemon=True).start()
    threading.Timer(1,open_browser).start()
    safe_put_queue({"type":"software","level":"info","data":"Hệ thống khởi động xong.Hiển thị trang web"})
    common_object.socketio.run(common_object.app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)
   



