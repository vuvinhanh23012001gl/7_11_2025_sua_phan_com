# 🧠 Smart Production Checker  
**Version:** 0.1  
**Author:** Vũ Vinh Ánh  
**Email:** anh.vu@example.com  
**License:** MIT  
**Created:** 2025-06-30 

#------------------------Mô tả phần mềm----------------------------
Dự án **Smart Production Checker** là phần mềm quản lý và kiểm tra sản phẩm tự động trong dây chuyền sản xuất.  
Được thiết kế để **tự động hóa và giám sát chất lượng sản phẩm**, giúp giảm lỗi thủ công và tăng năng suất.


📁----------------------- CẤU TRÚC THƯ MỤC & CHỨC NĂNG CHÍNH------------------------
Thư mục / File Mô tả chức năng
config/ Lưu các file cấu hình phần mềm (COM, camera, ngưỡng nhận diện, v.v.).
model/ Chứa các model nhận dạng, mô-đun xử lý ảnh, và thuật toán phân loại sản phẩm.
static/ Chứa file CSS, JS, hình ảnh phục vụ giao diện web Flask.
templates/ Chứa các file HTML giao diện web Flask.
test_js/ Thư mục test JavaScript (phục vụ kiểm thử, không bắt buộc khi build exe).
Camera_25129678.pfs File cấu hình camera, chứa thông số hoặc profile chụp.



------------------------File Chức năng------------------------
run.py Entry point – Chạy toàn bộ chương trình.
Tự động load config, kết nối camera, UART và chạy Flask server.
run_flask.bat File batch để chạy Flask app nhanh.
main_pc.py Điều phối luồng xử lý chính trên PC (kết nối camera, xử lý ảnh, giao tiếp STM32).
connect_camera.py Kết nối, khởi tạo và đọc ảnh từ camera.
erial_communication.py / manager_serial.py
Giao tiếp UART với STM32 (gửi lệnh điều khiển, nhận phản hồi).
common_value.py / common_object.py Chứa biến và lớp dùng chung trong toàn dự án (global settings, đối tượng chung).
config_software.py Đọc và ghi file cấu hình phần mềm.
func.py Các hàm tiện ích chung (xử lý chuỗi, ghi log, format dữ liệu…).
judget_product.py Thuật toán đánh giá sản phẩm OK / NG.
count_product_ok_ng.py Đếm số lượng sản phẩm đạt / lỗi.
folder_create.py Tạo và quản lý thư mục lưu kết quả, ảnh log, dữ liệu sản phẩm.
log.py, obj_log.py Quản lý ghi log hệ thống (lỗi, sự kiện, thông tin).
point_oil.py, point_oil_detected.py, point_oil_detected_manage.py
Xử lý và quản lý điểm dầu (phát hiện vùng, đo vị trí dầu trên sản phẩm).
process_master.py Xử lý dữ liệu gốc (master) để làm chuẩn cho việc so sánh sản phẩm.
master_circle_shape.py, master_rect_shape.py
Định nghĩa vùng kiểm tra hình tròn / hình chữ nhật cho sản phẩm mẫu.
producttype.py, producttypemanager.py
Quản lý loại sản phẩm, lưu thông tin cấu hình cho từng loại.
user.py Xử lý thông tin người dùng (nếu có phân quyền / lưu cấu hình cá nhân).
shared_queue.py Hàng đợi chia sẻ dữ liệu giữa các luồng (ví dụ: camera → xử lý ảnh → hiển thị).


⚙️#------------------------Phần này hướng dẫn cài đặt phần mềm cho kĩ thuật viên----------------------------

Tự động kết nối camera và cổng COM (UART) khi phần mềm khởi động.
Giao tiếp với STM32 để điều khiển cơ cấu chụp và xử lý ảnh sản phẩm.d
Quản lý người dùng (User / Admin) thông qua file JSON, hỗ trợ phân quyền thao tác.
Tải và lưu cấu hình phần mềm (COM, Camera, thông số nhận dạng, thư mục lưu dữ liệu).
Xử lý ảnh sản phẩm bằng OpenCV: phát hiện, so sánh với mẫu (master), phân loại OK / NG.
Lưu trữ kết quả kiểm tra (ảnh, log, dữ liệu thống kê) theo từng sản phẩm và ngày.
Giao diện Web được xây dựng bằng Flask hiển thị hình ảnh, kết quả và số lượng sản phẩm OK/NG.
Tự động đếm và ghi log sản phẩm trong suốt quá trình vận hành.
Hỗ trợ nhiều loại sản phẩm, mỗi loại có vùng kiểm tra và thông số riêng.
Khởi động nhanh bằng file run_flask.bat hoặc run.exe sau khi build.



#------------------------Phần này hướng dẫn cài đặt phần mềm cho kĩ thuật viên----------------------------
B1:Import các thư viện cần có từ file requirment.txt
B2:Phần mềm chạy từ File run.Nhấn run chạy thử nếu lỗi quay lại B1
B3:Sau khi đã chạy thành công, mở phần mềm lên để test các chức năng.Khi chạy file run.py phần mềm sẽ tự động load các thông số phần mềm
cấu hình,dữ liệu sản phẩm,tự động kết nối Camera,cổng COM,...
B4:Build file exe chạy bằng thư viện auto-py-to-exe.
B5:Vào đường dẫn file run ->Chạy terminal->Nhập câu lênh "auto-py-to-exe"->nhấn Enter->
Phần mềm sẽ show GUI để build->Nhấn vào đường dẫn "Browse"->Trỏ đến file run.py ->
Chọn Additional Files -> Add Folder -> Sau đó trỏ đến đường dẫn Folder "config,static,template,model".test_js la file test không cần thêm
B6.Nhấn CONVERT .PY.TO.exe
B7.Sau khi build file thành công chạy file run.exe trong thư mục OUTPUT.Và tiến hành chạy thử nếu chạy thử không thành công là do thiếu thư viện 
python mà lúc chuyển sang exe Gui chưa tìm được tiến hành thêm thư viện B7
B7.Nhập cmd lệnh "python -m site" để lấy đường dẫn lưu các gói packages thư viện python
B8. Thư viện nằm trong có dạng thư mục tùy máy tính
'C:\\Users\\vuthi\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages'
B9:Copy những thư viện mà show log báo lỗi thiếu vào Folder OUTOUT/__internal__.
B10.Chạy phần mềm ok
C:\Users\anhuv\AppData\Local\Programs\Python\Python313\Lib\site-packages

# Model → load 1 lần duy nhất khi khởi động phần mềm.
# Master data (shape, quy định) → load khi chọn ID sản phẩm hoặc khi người dùng thay đổi quy chuẩn.
# Detection data (kết quả model trên từng ảnh) → luôn tạo mới cho từng ảnh.
# main_pc.click_page_html = 4  --> Là vào thêm sản phẩm mới
# main_pc.click_page_html = 1  --> Là vào trang main chính
# main_pc.click_page_html = 3  --> Là lấy master 
# main_pc.click_page_html = 2  --> Training model
# main_pc.click_page_html = 5  --> Choose master
# main_pc.click_page_html = 6  --> Add master
# main_pc.click_page_html = 7  --> Thay đổi cồng COM
# main_pc.click_page_html = 8 # Câu hình cổng camera

