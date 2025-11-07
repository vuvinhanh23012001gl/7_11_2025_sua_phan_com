
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn /  Module Folder
# Description: Manager Folder
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
from datetime import datetime
from typing import Dict,Any
from pathlib import Path
import json
import os
import shutil
import openpyxl  # thư viện tạo file Excel
import cv2
from obj_log import safe_put_queue,debug_print
from common_value import NAME_FILE_STATIC

class Create:
    """Lớp hỗ trợ tạo và quản lý thư mục, file, và thao tác với JSON."""
    def __init__(self,base_path: str = None):
        self.base_path = base_path
        
    def get_data_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
        """Trả về data sản phẩm hiện tại ở trong neu chua khoi tao thi se khoi tao duong dan
           Trả về rỗng nếu không có dữ liệu trong file
        """
        try: 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            debug_print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    debug_print(f"📄 Tạo file JSON mới: {file_json}")
                    return None 
            with open(file_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.data = data
                debug_print("✅ Đọc JSON thành công")
                return data
        except Exception as e:
            debug_print("⚠️ File JSON rỗng hoặc sai định dạng → trả về dict rỗng")
            return {}
        
    def save_image_grandaugter(self, image, file_name: str, parent: str, grandparent: str, extension: str = "jpg") -> str:
        """
        Lưu ảnh (numpy.ndarray) vào thư mục theo cấu trúc: grandparent/parent/file_name.extension
        - image: ảnh numpy.ndarray
        - file_name: tên file (không cần phần mở rộng)
        - parent: thư mục con (VD: tên sản phẩm)
        - grandparent: thư mục cha (VD: static/Master_Photo)
        - extension: định dạng ảnh ('jpg', 'png', ...)
        Trả về: đường dẫn ảnh đã lưu (str)
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dir_grandparent = os.path.join(current_dir, grandparent)
        dir_parent = os.path.join(dir_grandparent, parent)
        os.makedirs(dir_parent, exist_ok=True)

        file_path = os.path.join(dir_parent, f"{file_name}.{extension}")

        if cv2.imwrite(file_path, image):
            debug_print(f"📸 Lưu ảnh thành công: {file_path}")
            return file_path
        else:
            debug_print(f"⚠️ Lưu ảnh thất bại: {file_path}")
            return ""
        
    def get_data_in_path(self,path:str):
         """đọc File json theo đường dẫn nếu không có trả về False nếu không có  file hoặc 
         có đường dẫn nhưng không phải file json . nếu thỏa mãn hết tất cả trả về data của đường dẫn
         """
         if path.lower().endswith(".json"):
            debug_print("Là file Json")
         else:
             return False
         if not os.path.exists(path):
               debug_print("Thư mục này không tồn tại")
               return False
         else :
            with open(path, 'r', encoding='utf-8') as f:
                debug_print("Đọc File thành cônng")
                return json.load(f)

    def get_path_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
            """Giống với hàm trên nhưng trả về đường dẫn tới thu mục con
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            debug_print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    debug_print(f"📄 Tạo file JSON mới: {file_json}")
            return file_json 

    def delete_folder(self,file_path):
        """
        Xóa file hoặc thư mục nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu không xóa được.
        """
        if not os.path.exists(file_path):
            debug_print(f"File/Thư mục không tồn tại: {file_path}")
            return False

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                debug_print(f"File đã xóa: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                debug_print(f"Thư mục đã xóa: {file_path}")
            else:
                debug_print(f"Không phải file hay thư mục: {file_path}")
                return False
            return True
        except PermissionError:
            debug_print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            debug_print(f"Lỗi khi xóa '{file_path}': {e}")
            return False
        
    def delete_file(self,file_path):
        """
        Xóa file nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu thất bại.
        """
        if not os.path.exists(file_path):
            debug_print(f"File không tồn tại: {file_path}")
            return False

        if not os.path.isfile(file_path):
            debug_print(f"'{file_path}' không phải là file")
            return False

        try:
            os.remove(file_path)
            debug_print(f"Đã xóa file: {file_path}")
            return True
        except PermissionError:
            debug_print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            debug_print(f"Lỗi khi xóa file '{file_path}': {e}")
            return False
        
    def find_file_in_folder(self,folder_path, filename):
        """
        Tìm file trong thư mục.
        folder_path: đường dẫn thư mục
        filename: tên file muốn tìm (exact match)
        Trả về đường dẫn đầy đủ nếu tìm thấy, None nếu không tìm thấy
        """
        if not os.path.exists(folder_path):
            debug_print(f"Thư mục không tồn tại: {folder_path}")
            return None

        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path) and f == filename:
                return full_path

        debug_print(f"Không tìm thấy file '{filename}' trong '{folder_path}'")
        return None
    
    def create_file_in_folder(self, folder_path: str, file_name: str) -> Path | bool:
        """
        Tạo một file mới trong folder_path với tên file_name.
        - Nếu file chưa tồn tại: tạo file, trả về Path.
        - Nếu file đã tồn tại: trả về False.
        - Nếu không tạo được file: trả về false.
        """
        try:
            folder = Path(folder_path)
            folder.mkdir(parents=True, exist_ok=True)  # đảm bảo folder tồn tại

            file_path = folder / file_name
            if not file_path.exists():
                file_path.touch()  # tạo file rỗng
                debug_print(f"Đã tạo file: {file_path}")     
                return {"return":True,"path":file_path}
            else:
                debug_print(f"File đã tồn tại: {file_path}")
                return {"return":False,"path":file_path}
            
        except Exception as e:
            debug_print(f"❌ Không thể tạo file: {e}")
            return False
        
    def create_file_in_folder_two(self,name_file: str, name_folder: str):
            """Tạo ra 1 foder nếu có rồi thì vào đó tạo ra 1 file
             trả về đường dẫn đến file nằm trong folder
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            target_dir = os.path.join(current_dir, name_folder)
            os.makedirs(target_dir, exist_ok=True)

            file_path = os.path.join(target_dir, name_file)

            if not os.path.exists(file_path):
                debug_print("📄 File không tồn tại, tạo mới.")
                with open(file_path, "wb") as f:   
                    debug_print("File rỗng")
                    f.write(b"")                   
            return file_path

    def read_file_in_path(self,path):
        """
        Đọc toàn bộ nội dung file text theo đường dẫn và trả về chuỗi.
        Nếu file không tồn tại, trả về False.
        """
        import os

        if not os.path.isfile(path):
            debug_print(f"File '{path}' không tồn tại.")
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                noi_dung = f.read()
            return noi_dung
        except Exception as e:
            debug_print(f"Lỗi khi đọc file: {e}")
            return False
        
    def get_path_same_level(self,name_find):
        """
        Tìm file 'name_find' trong cùng thư mục với file script.
        Trả về đường dẫn đầy đủ nếu tìm thấy, False nếu không tìm thấy.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isfile(item_path) and item == name_find:
                return item_path  # trả về full path nếu tìm thấy

        return False  # không tìm thấy file
    
    def create_folder_peer(self,name_folder: str) -> str:
        """
        Tạo một thư mục cùng cấp với file đang chạy.
        Nếu thư mục đã tồn tại, vẫn trả về đường dẫn.
        Trả về đường dẫn tuyệt đối của thư mục.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, name_folder)
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            debug_print(f"✅ Thư mục đã tạo hoặc đã tồn tại: {folder_path}")
        except Exception as e:
            debug_print(f"❌ Lỗi khi tạo folder: {e}")
            return None
        return folder_path   
    
    def create_subfolder(self,parent_path: str, child_name: str) -> str:
        """
        Tạo một thư mục con trong thư mục cha.
        Nếu đã tồn tại, không báo lỗi nhưng vẫn trả về đường dẫn.
        Trả về đường dẫn tuyệt đối của thư mục con.
        """
        # Kết hợp đường dẫn cha + con
        folder_path = os.path.join(parent_path, child_name)
        
        try:
            os.makedirs(folder_path, exist_ok=True)  # tạo nếu chưa tồn tại
        except Exception as e:
            debug_print(f"❌ Lỗi khi tạo thư mục con: {e}")
            return None
        
        # Trả về đường dẫn tuyệt đối
        return os.path.abspath(folder_path)

    def create_folder(self,folder_path: str):
        """
        Tạo 1 folder theo đường dẫn.
        Nếu đã tồn tại thì không báo lỗi.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            debug_print(f"✅ Đã tạo (hoặc đã tồn tại): {folder_path}")
            return folder_path
        except Exception as e:
            debug_print(f"❌ Lỗi khi tạo folder: {e}")
            return None
    def save_json(self,data: Dict[str, Any], filename: str) -> None:
        """
        Ghi dữ liệu vào file JSON
        :param data: dictionary cần ghi
        :param filename: tên file .json
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_json(self,filename: str) -> Dict[str, Any]:
        """
        Đọc dữ liệu từ file JSON
        :param filename: tên file .json
        :return: dictionary dữ liệu đọc được
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            debug_print(f"⚠️ File '{filename}' không tồn tại.")
            return {}
        except json.JSONDecodeError:
            debug_print(f"⚠️ File '{filename}' không đúng định dạng JSON.")
            return {}
        
    def read_json_from_file(self, file_path: str) -> dict:
        """
        Đọc dữ liệu JSON từ file và trả về dạng dict.
        - file_path: đường dẫn tới file JSON
        """
        try:
            # Nếu file chưa tồn tại -> trả về dict rỗng
            if not os.path.exists(file_path):
                debug_print(f"⚠️ File không tồn tại: {file_path}")
                return {}

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # print(f"✅ Đã đọc JSON từ: {file_path}")
                return data

        except json.JSONDecodeError as e:
            debug_print(f"❌ Lỗi định dạng JSON ({file_path}): {e}")
            return {}
        except Exception as e:
            debug_print(f"❌ Lỗi khi đọc file JSON: {e}")
            return {}
        
    def write_data_to_file(self, file_path: str, data: bytes, mode: str = "ab"):
        """
        Ghi dữ liệu vào file.
        - file_path: đường dẫn đến file
        - data: dữ liệu cần ghi (bytes hoặc string)
        - mode: chế độ ghi ('ab' = append binary, 'wb' = ghi đè binary)
        """
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Nếu là string thì encode sang bytes
            if isinstance(data, str):
                data = data.encode("utf-8")

            with open(file_path, mode) as f:
                f.write(data)
                debug_print(f"✅ Đã ghi {len(data)} byte vào: {file_path}")

        except Exception as e:
            debug_print(f"❌ Lỗi khi ghi file: {e}")

    def write_data_to_file_in_folder_static(self,filename: str, content: str, append: bool = False) -> None:
        """
        Ghi dữ liệu vào file trong thư mục static.
        - append = False: ghi đè nội dung file
        - append = True: ghi thêm vào cuối file
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            static_dir = os.path.join(current_dir, NAME_FILE_STATIC)
            os.makedirs(static_dir, exist_ok=True)
            file_path = os.path.join(static_dir, filename)
            mode = "a" if append else "w"
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(str(content))
            action = "Thêm vào" if append else "Ghi đè"
            debug_print(f"✅ {action} file '{filename}' thành công.")
        except:
            debug_print(f"X {action} file '{filename}' lỗi thành công.")

    def write_json_to_file(self, file_path: str, data: dict, indent: int = 4):
        """
        Ghi dữ liệu dạng JSON vào file.
        - file_path: đường dẫn tới file json
        - data: dict hoặc list cần lưu
        - indent: số khoảng trắng khi format cho dễ đọc
        """
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
                debug_print(f"✅ Đã ghi JSON vào: {file_path}")

        except Exception as e:
            debug_print(f"❌ Lỗi khi ghi file JSON: {e}")

    def get_or_create_json(self, name_file: str, name_folder: str) -> str:
        """
        Kiểm tra nếu file JSON đã tồn tại thì trả về đường dẫn.
        Nếu chưa có: tạo folder, tạo file và ghi {} rỗng.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir  = os.path.join(current_dir, name_folder)
        os.makedirs(target_dir, exist_ok=True)  # đảm bảo folder tồn tại

        file_path = os.path.join(target_dir, name_file)

        if not os.path.exists(file_path):
            debug_print(f"📂 Chưa có file, tạo mới: {file_path}")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                debug_print("✅ Đã tạo file JSON rỗng {}")
            except Exception as e:
                debug_print("❌ Lỗi khi tạo file JSON:", e)
        else:
            debug_print(f"✅ File đã tồn tại: {file_path}")

        return file_path
    
    def get_list_file_in_folder(self,folder_path: str) -> list:
        """Trả về danh sách các file có trong folder (không gồm thư mục con)."""
        if not os.path.exists(folder_path):
            return []
        return [file for file in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file))]
    
    def get_list_folder_in_folder(self, folder_path: str) -> list:
        """Trả về danh sách các thư mục con có trong folder (không gồm file)."""
        if not os.path.exists(folder_path):
            return []
        return [name for name in os.listdir(folder_path)
                if os.path.isdir(os.path.join(folder_path, name))]
    
    def create_file_log(self,path_save_log_excell,formart="xlsx",name_file=None):
        """
        Trả về đường dẫn đầy đủ của file Excel.
        Nếu không truyền name_file, sẽ tạo tên file theo thời gian hiện tại.
        Nếu file chưa tồn tại, hàm sẽ tạo file Excel rỗng.
        """
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(path_save_log_excell):
            os.makedirs(path_save_log_excell)

        # Tạo tên file theo timestamp nếu chưa có
        if name_file is None:
            now = datetime.now()
            # Dùng '-' thay ':' vì Windows không cho phép ':' trong tên file
            name_file = f"log_{now.strftime('%Y%m%d_%H-%M-%S')}.{formart}"

        file_path = os.path.join(path_save_log_excell, name_file)

        # Nếu file chưa tồn tại, tạo file Excel rỗng
        if not os.path.exists(file_path):
            wb = openpyxl.Workbook()
            wb.save(file_path)
        return file_path
    
    def create_file_log_img(self,img, path_save_log_img, file_name=None, extension="jpg"):
        """
        Tạo file ảnh (placeholder) trong folder path_save_log_img.
        - img: ảnh numpy array
        - path_save_log_img: đường dẫn folder lưu ảnh
        - file_name: tên file (không cần phần mở rộng), nếu None thì tạo theo timestamp
        - extension: 'jpg' hoặc 'png'
        
        Trả về: đường dẫn file ảnh đã tạo
        """
        if path_save_log_img is None:
            debug_print("Bạn cần truyền đường dẫn folder hợp lệ!")
        
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(path_save_log_img):
            os.makedirs(path_save_log_img)

        # Tạo tên file theo timestamp nếu chưa có
        if file_name is None:
            now = datetime.now()
            file_name = f"img_{now.strftime('%y%m%d_%H%M%S')}_{now.microsecond // 1000:03d}"

        file_path = os.path.join(path_save_log_img, f"{file_name}.{extension}")
        cv2.imwrite(file_path, img)
        debug_print(f"📸 Tạo file ảnh thành công: {file_path}")
        return file_path
    
    
    def create_file_text_log(self, folder_path, extension="txt", name_file=None):
        """
        Tạo file log text (dùng cho logging module).
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if name_file is None:
            now = datetime.now()
            name_file = f"log_{now.strftime('%Y%m%d_%H-%M-%S')}.{extension}"

        file_path = os.path.join(folder_path, name_file)

        if not os.path.exists(file_path):
            # ✅ Tạo file text rỗng
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")  

        return file_path

    def find_file(self,path, filename):
        """Tìm file trong đường dẫn.
        Trả về đường dẫn đầy đủ nếu tìm thấy, False nếu không tìm thấy."""
        file_path = os.path.join(path, filename)
        return file_path if os.path.exists(file_path) else False
    
    def get_old_folders_by_threshold(self,prefix: str, folders: list, days_threshold=30):
        """
        Lọc ra danh sách folder có dạng 'prefixYYYY-MM-DD'
        và có ngày cũ hơn 'days_threshold' ngày so với folder mới nhất.

        Ví dụ folder: data_2025-10-26
        """
        if not folders:
            return []

        folder_dates = {}
        for f in folders:
            try:
                if f.startswith(prefix):
                    # lấy phần ngày trong tên folder (sau prefix)
                    date_str = f[len(prefix):]
                    dt = datetime.strptime(date_str, '%Y-%m-%d')
                    folder_dates[f] = dt
            except Exception as e:
                debug_print(f"Lỗi parse {f}: {e}")

        if not folder_dates:
            return []

        # tìm ngày mới nhất
        latest_date = max(folder_dates.values())

        # lọc ra folder cũ hơn days_threshold
        old_folders = [f for f, dt in folder_dates.items()
                    if (latest_date - dt).days > days_threshold]

        return old_folders
    def create_folder_in_static(self,subfolder_name: str) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(current_dir,NAME_FILE_STATIC)
        subfolder_path = os.path.join(static_dir, subfolder_name)

        # Tạo folder cha (static) và folder con
        os.makedirs(subfolder_path, exist_ok=True)

        debug_print(f"📁 Đã tạo thư mục: {subfolder_path}")
        return subfolder_path
    def get_image_paths_from_folder(self,folder_path: str) -> list:
        """
        Trả về danh sách đường dẫn ảnh trong thư mục theo đúng thứ tự số (img_0, img_1, img_2,...)
        """
        image_paths = []

        abs_folder_path = os.path.join(os.path.dirname(__file__), folder_path)

        if os.path.exists(abs_folder_path) and os.path.isdir(abs_folder_path):
            # Lấy danh sách file, sắp xếp theo số thứ tự trong tên file
            files = sorted(
                os.listdir(abs_folder_path),
                key=lambda x: int(x.split('_')[-1].split('.')[0]) if '_' in x and x.split('_')[-1].split('.')[0].isdigit() else x
            )

            for file in files:
                file_path = os.path.join(abs_folder_path, file)
                if os.path.isfile(file_path):
                    normalized_path = os.path.join(folder_path, file).replace("\\", "/")
                    image_paths.append(normalized_path)

        return image_paths
    
    def read_data_from_file(self,filename: str) -> str:
        """
        Đọc toàn bộ nội dung từ file trong thư mục static có tên là filename
        Trả về chuỗi nội dung, hoặc chuỗi rỗng nếu file không tồn tại.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(current_dir, NAME_FILE_STATIC)
        file_path = os.path.join(static_dir, filename)
        if not os.path.exists(file_path):
            debug_print(f"❌ File '{filename}' không tồn tại.")
            return ""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            debug_print(f"📄 Đọc nội dung từ file '{filename}' thành công.")
            return content
    def clear_file_content(self,filename: str) -> None:
        """
        Làm rỗng nội dung file (giữ lại file nhưng xóa toàn bộ dữ liệu bên trong).
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(current_dir, NAME_FILE_STATIC)
        file_path = os.path.join(static_dir, filename)

        if os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.truncate(0)  # Xóa toàn bộ nội dung
            debug_print(f"🧹 Đã xóa toàn bộ nội dung trong file '{filename}'.")
        else:
            debug_print(f"❌ File '{filename}' không tồn tại để xóa nội dung.")
    def create_choose_master(self,name_location_save_in_static: str):
        """Hàm này sẽ luôn tạo 1 file nằm trong static/name_location_save_in_static nếu không có thì nó sẽ tạo vào khởi giá trị
        ban đầu là 0 nếu có rồi thì nó sẽ không làm gì cả
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(current_dir, NAME_FILE_STATIC)
        os.makedirs(static_dir, exist_ok=True)
        file_path = os.path.join(static_dir, name_location_save_in_static)
        if not os.path.exists(file_path):
            debug_print("File không tồn tại, tạo mới.")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("0")
        else:
            debug_print("File đã tồn tại, sẽ đọc nội dung.")
