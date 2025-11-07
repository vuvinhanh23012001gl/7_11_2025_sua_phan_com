# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn /  Module Count Product OK/NG
# Description: Module Count Product OK/NG
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
import common_value 
class Count():
    
    """Lớp để đếm số lượng sản phẩm OK và NG, lưu trữ dữ liệu vào file JSON."""
    from folder_create import Create
    obj_folder = Create()
    NAME_FILE_COUNT_PRODUCT = "count.json"
    NAME_VALUE_OK = "product_ok"
    NAME_VALUE_NG = "product_ng"
    path_file_count = obj_folder.get_or_create_json(NAME_FILE_COUNT_PRODUCT,common_value.NAME_FILE_STATIC)

    def __init__(self):
        self.OK = 0
        self.NG = 0
        self.default_data_if_file_emptry()

    def read_data(self):
        """Đọc dữ liệu số lượng sản phẩm OK và NG từ file JSON."""
        return self.OK,self.NG
    
    def write_data(self,OK,NG):
        """Ghi dữ liệu số lượng sản phẩm OK và NG vào file JSON."""
        self.OK = OK
        self.NG = NG
        data_write = {
            Count.NAME_VALUE_OK: self.OK,
            Count.NAME_VALUE_NG: self.NG,
        }
        Count.obj_folder.write_json_to_file(Count.path_file_count,data_write)

    def default_data_if_file_emptry(self):
        """Khởi tạo dữ liệu mặc định nếu file JSON trống hoặc không tồn tại."""
        data = Count.obj_folder.read_json_from_file(Count.path_file_count)
        self.OK = data.get( f"{Count.NAME_VALUE_OK}",0)
        self.NG = data.get(f"{Count.NAME_VALUE_NG}",0)

    def reset(self):
        """Đặt lại số lượng sản phẩm OK và NG về 0."""
        self.OK = 0
        self.NG = 0
        self.write_data(self.OK,self.NG)

    def increase_ok(self, value=1):
        """Tăng số lượng sản phẩm OK"""
        self.OK += value
        self.write_data(self.OK, self.NG)

    def increase_ng(self, value=1):
            """Tăng số lượng sản phẩm NG"""
            self.NG += value
            self.write_data(self.OK, self.NG)

#==================================Hàm chạy kiểm thử====================================================#

# count_produc  = Count()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.reset()





        




    
        










