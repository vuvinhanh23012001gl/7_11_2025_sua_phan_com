# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module Account
# Description: Log in ,Sign in,Create User,admin
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------

from folder_create import Create
import common_value
from obj_log import safe_put_queue,debug_print

USER_ADMIN = "BIVNRDP"
PASSWORD_ADMIN = "BIVNRDP"

class acc_use():
    """Lớp này dành cho User"""
    def __init__(self,user_name ="None",use_password="None",first_name="None",last_name="None",line="None",usine="None"):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.line = line
        self.usine = usine
        self.user_name = user_name
        self.use_password = use_password

    def show_infor_user(self):
        """Hiển thị toàn bộ thông tin của user."""
        debug_print("===== USER INFORMATION =====")
        debug_print("First Name:", self.first_name)
        debug_print("Last Name:", self.last_name)
        debug_print("Username:", self.user_name)
        debug_print("Password:", self.use_password)
        debug_print("Line:", self.line)
        debug_print("Usine:", self.usine)
        debug_print("============================")

    def to_dict(self):
        """Chuyển thông tin user thành dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "use_password": self.use_password,
            "line": self.line,
            "usine": self.usine
        }

# user = acc_use()
# user.show_infor_user()


class acc_admmin():

    """Lớp này dành cho Admin"""
    def __init__(self,admin_name = USER_ADMIN,admin_password=PASSWORD_ADMIN):
        self.admin_name = admin_name
        self.admin_password = admin_password
    def show_infor_use(self):
        """In thong tin tai khoan mat khau cua user """
        debug_print("User:",self.admin_name)
        debug_print("Password:",self.admin_password)
    def to_dict(self):
        """Chuyển thông tin admin thành dictionary."""
        return {
            "admin_name": self.admin_name,
            "admin_password": self.admin_password
        }


class Manage_User():

    """Lớp này là lớp quản lý tài khoản user và admin"""
    object_folder =  Create()
    NAME_FILE_JSON_USER  = "acc_user.json" 
    NAME_FILE_JSON_ADMIN =  "acc_admin.json"
    path_admin = object_folder.get_path_grandaugter(NAME_FILE_JSON_ADMIN,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)
    path_user = object_folder.get_path_grandaugter(NAME_FILE_JSON_USER,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)

    def __init__(self):
        self.data_use = [] 
        self.data_admin = {}
        self.current_account = {}  #Trả về thông tin người hiện tại đăng nhập

    def create_user(self, user_name:str=None, use_password:str=None, first_name:str=None, last_name:str=None, line:str=None, usine:str=None):
        """Hàm này tạo ra tài khoản user"""
        if not all([user_name, use_password, first_name, last_name, line, usine]):
            debug_print("Thiếu dữ liệu khi tạo tài khoản User")
            safe_put_queue({"type":"software","level":"info","data":f"Tạo tài khoản thất bại người dùng nhập thiếu thông tin đăng nhập."})
            return False,"Thiếu dữ liệu khi tạo tài khoản"
        arr_user = []
        object_user = acc_use(user_name,use_password,first_name, last_name,line,usine)
        self.data_use = Manage_User.object_folder.get_data_grandaugter(Manage_User.NAME_FILE_JSON_USER,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)  # cap nhat truoc khi thay
        if self.data_use:
            for acc in self.data_use:
                user_name_file = acc.get("user_name",None)
                if user_name_file:
                    if user_name_file.strip() == user_name.strip():
                        safe_put_queue({"type":"software","level":"info","data":f"Tạo tài khoản thất bại do đã tồn tại {user_name} {use_password} {first_name}{last_name}{line}{usine}"})
                        return False,"Tài khoản này đã tồn tại"
            self.data_use.append(object_user.to_dict())  #cap nhat du lieu moi
            Manage_User.object_folder.save_json(self.data_use,Manage_User.path_user) # luu du lieu moi vao file
            debug_print(f"Lưu {user_name} thành công vào list File User")
            safe_put_queue({"type":"software","level":"info","data":f"Tạo tài khoản thành công {user_name} {use_password} {first_name}{last_name}{line}{usine}"})
            return True,"Tạo thành công tài khoản"
        else:
            arr_user.append(object_user.to_dict())
            Manage_User.object_folder.save_json(arr_user,Manage_User.path_user)
            debug_print(f"Lưu {user_name} vào phần tử đầu tiên trong list File User")
            safe_put_queue({"type":"software","level":"info","data":f"Tạo tài khoản đầu tiên thành công {user_name} {use_password} {first_name}{last_name}{line}{usine}"})
            return True,"Tạo thành công tài khoản"
        
    def delete_user(self, user_name: str):
        """Xóa user theo user_name"""
        if not user_name:
            debug_print("Chưa cung cấp user_name để xóa")
            return False

        # Load dữ liệu user hiện tại
        self.data_use = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_USER,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )

        if not self.data_use:
            debug_print("Danh sách user đang trống, không thể xóa")
            return False

        # Tìm và xóa user
        new_data_use = [user for user in self.data_use if user.get("user_name", "").strip() != user_name.strip()]

        if len(new_data_use) == len(self.data_use):
            debug_print(f"Không tìm thấy user {user_name} để xóa")
            return False

        # Lưu lại file JSON sau khi xóa
        Manage_User.object_folder.save_json(new_data_use, Manage_User.path_user)
        debug_print(f"Xóa user {user_name} thành công")
        safe_put_queue({"type":"software","level":"info","data":f"Xóa User {user_name} thành công"})
        return True
    
    def create_admin(self, admin_name: str = "", admin_password: str = None):
        """Hàm này tạo ra tài khoản admin"""
        if not all([admin_name,admin_password]):
            debug_print("Thiếu dữ liệu khi tạo tài khoản Admin tạo tài khoản admin mặc định")
            obj_acc_admmin = acc_admmin()
            self.data_admin  = obj_acc_admmin.to_dict()
            Manage_User.object_folder.save_json(self.data_admin,Manage_User.path_admin) # luu du lieu moi vao file
        if admin_name and admin_password:
            obj_acc_admmin = acc_admmin(admin_name,admin_password)
            self.data_admin  = obj_acc_admmin.to_dict()
            Manage_User.object_folder.save_json(self.data_admin,Manage_User.path_admin) # luu du lieu moi vao file

    def check_account(self, account_name: str, password: str):
        """
        Kiểm tra tài khoản:
        - Nếu tồn tại trả về (True, True) nếu admin
        - Trả về (True, False) nếu user
        - Nếu không tồn tại trả về (False, False)
        """
        # Kiểm tra admin
        self.data_admin = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_ADMIN,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        if self.data_admin:
            if (self.data_admin.get("admin_name", "").strip() == account_name.strip() and
                self.data_admin.get("admin_password", "") == password):
                self.current_account = self.get_account_info_by_name(account_name)
                safe_put_queue({"type":"software","level":"info","data":f"Admin đăng nhập"})
                return True, True

        # Kiểm tra user
        self.data_use = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_USER,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        debug_print(" self.data_use", self.data_use)
        if self.data_use:   
            for user in self.data_use:
                if (user.get("user_name", "").strip() == account_name.strip() and
                    user.get("use_password", "") == password):
                    first_name = user.get("first_name", "") 
                    last_name = user.get("last_name", "") 
                    safe_put_queue({"type":"software","level":"info","data":f"User đăng nhập tên người dùng: {first_name} {last_name} Tài khoản:{user.get("user_name", "").strip()}"})
                    self.current_account = self.get_account_info_by_name(account_name)
                    return True, False
        self.current_account = {}
        return False, False

    def get_account_info_by_name(self, account_name: str):
        """
        Trả về dict thông tin tài khoản khi nhập vào account_name (không cần password)
        - Nếu là admin → trả về dict admin
        - Nếu là user → trả về dict user
        - Nếu không tồn tại → trả về {}
        """
        if not account_name:
            debug_print("Chưa nhập account_name")
            return {}

        # --- Kiểm tra admin ---
        self.data_admin = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_ADMIN,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        if self.data_admin:
            if self.data_admin.get("admin_name", "").strip() == account_name.strip():
                debug_print(f"Tìm thấy tài khoản Admin: {account_name}")
                return {
                    "type": "admin",
                    **self.data_admin
                }

        # --- Kiểm tra user ---
        self.data_use = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_USER,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        if self.data_use:
            for user in self.data_use:
                if user.get("user_name", "").strip() == account_name.strip():
                    debug_print(f"Tìm thấy tài khoản User: {account_name}")
                    return {
                        "type": "user",
                        **user
                    }

        # --- Không tìm thấy ---
        debug_print(f"Không tìm thấy tài khoản: {account_name}")
        return {}
    def get_current_account(self):
        """
        Trả về thông tin tài khoản người đăng nhập hiện tại.
        Nếu chưa đăng nhập hoặc đăng nhập sai → trả về {}
        """
        if self.current_account:
            return self.current_account
        else:
            debug_print("Chưa có người đăng nhập.")
            return {}


#==================================Hàm chạy kiểm thử====================================================#
# manager_one = Manage_User()
# # debug_print(manager_one.get_account_info_by_name("3"))
# debug_print(manager_one.check_account("3","1"))
# debug_print(manager_one.get_current_account())
# manager_one.delete_user("user_name21")
# manager_one.create_admin()


    
