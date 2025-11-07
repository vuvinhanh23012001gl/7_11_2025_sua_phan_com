
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module serial
# Description:  Open,send function,receive function
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------

import serial.tools.list_ports
from folder_create import Create
from common_value import NAME_FOLDER_CONFIG
from obj_log import safe_put_queue,debug_print

class Serial_Com:

    create_folder =  Create()
    NAME_FILE_CONFIG_COM_MONITOR = "config_com_port.json"
    path_folder_config = create_folder.get_or_create_json(NAME_FILE_CONFIG_COM_MONITOR,NAME_FOLDER_CONFIG)

    def __init__(self):
        
        self.ser = None 
        self.port = None
        self.baudrate = None
        self.bytesize = None
        self.parity =None
        self.stopbits = None
        self.timeout = None
        self.reconnect_interval = None
        self.Init()

    def setting_value_com(self,data):
            """Hàm này cài đặt thông số ban đầu cho cổng com"""
            self.port = data.get("device_port",None)
            self.baudrate = data.get("baudrate",115200)
            self.bytesize = data.get("bytesize", serial.EIGHTBITS)
            self.parity = data.get("parity", serial.PARITY_NONE)
            self.stopbits = data.get("stopbits",serial.STOPBITS_ONE)
            self.timeout = data.get("timeout", 1)
            self.reconnect_interval = data.get("reconnect_interval",1)

    def Init(self):

        """Init các thông số của cổng com vào các biến đoc và kiểm tra từ file"""
        data_config = self.read_serial_config()
        # debug_print(data_config)
        satus_check_data = self.check_enough_data(data_config)
        self.setting_value_com(data_config)
        if satus_check_data:
            debug_print(" self.port được cài đặt thông số cấu hinh")
            return True
        else:
            debug_print("self.port chưa được cài đặt  thông số ")
            return False
            
    def read_serial_config(self):
        return Serial_Com.create_folder.read_json_from_file(Serial_Com.path_folder_config)

    def check_enough_data(self,data):
        if data:
            device_port = self.get_config_value(data, "device_port")   #device_port co the bang none la loi
            baudrate = self.get_config_value(data, "baudrate")
            bytesize = self.get_config_value(data, "bytesize")
            parity = self.get_config_value(data, "parity")
            stopbits = self.get_config_value(data, "stopbits")
            timeout = self.get_config_value(data, "timeout")
            reconnect_interval = self.get_config_value(data, "reconnect_interval")
            if device_port == -1 or baudrate == -1 or bytesize == -1 or parity == -1 or stopbits == -1 or timeout == -1 or reconnect_interval == -1:
                return False
            return True
        debug_print("Dữ liệu không đủ check dữ liệu config = False")
        return False
    def get_config_value(self,data, key):
        """Trả về data của dict"""
        return data.get(key, -1)
    
    def open_port(self):
        """Mở port khi mới vào chương trình"""
        if self.port and self.ser is None:
            try:
                # print(f"Tiến hành mở cổng {self.port}")
                debug_print(self.port,self.baudrate,self.bytesize,self.parity,self.stopbits,self.timeout)
                self.ser = serial.Serial(
                    port = self.port,
                    baudrate=self.baudrate,
                    bytesize=self.bytesize,
                    parity=self.parity,
                    stopbits=self.stopbits,
                    timeout=self.timeout
                )
                safe_put_queue({"type":"software","level":"info","data":f"Mở cổng tự động thành công {self.port} baudrate {self.baudrate}"})
                debug_print("Mở tự động thành công")
                return True
            except Exception as e:
                safe_put_queue({"type":"software","level":"error","data":f"Mở cổng {self.port} thất bại: {str(e)}"})
                debug_print("Thiết bị chưa được cắm hoặc cổng bị lỗi hoặc tên cổng khác với số cổng thực tế")
                return False
        elif self.ser and self.port:
            debug_print("Cổng Ser và Port đang mở không mở lại")
            safe_put_queue({"type":"software","level":"warning","data":f"Cổng {self.port} đã mở, bỏ qua mở lại."})
            return True 
        if self.port is None and self.ser is None: 
            debug_print("Không tồn tại Port va Ser deu tat")
            safe_put_queue({"type":"software","level":"error","data":"Không tồn tại port và ser đều tắt"})
            return False  
        
    def open_port_setting(self,name_port_input,baudrate_input):
        """Mở port khi vào dùng hàm"""
        if  self.ser is None:
            try:
                # print(f"Tiến hành mở cổng {self.port}")
                # debug_print(self.port,self.baudrate,self.bytesize,self.parity,self.stopbits,self.timeout)
                ser = serial.Serial(
                    port = name_port_input,
                    baudrate= baudrate_input,
                    bytesize=self.bytesize,
                    parity=self.parity,
                    stopbits=self.stopbits,
                    timeout=self.timeout
                )
                # update lai du lieu
                self.ser = ser
                self.baudrate = baudrate_input
                self.port = name_port_input
                safe_put_queue({
                    "type": "software",
                    "level": "info",
                    "data": f"Mở cổng COM thủ công {name_port_input} baudrate {baudrate_input} thành công!"})
                
                debug_print("Mở COM thủ công thành công")
                return True
            except Exception as e:
                safe_put_queue({
                "type": "software",
                "level": "error",
                "data": f"Không thể mở cổng {name_port_input} ({e}) — thiết bị chưa được cắm hoặc cổng bị lỗi!"})
            
                debug_print("Thiết bị chưa được cắm hoặc cổng bị lỗi hoặc tên cổng khác với số cổng thực tế")
                return False
        if self.ser: 
            debug_print("Cổng com dã tồn tại")
            safe_put_queue({
            "type": "software",
            "level": "warning",
            "data": f"Cổng {self.port} đã được mở trước đó, bỏ qua thao tác mở lại."})
                
            return True  
    def  status_com(self,name_port):
       com_connecting = self.check_port(name_port)
       busy_gate   = self.is_com_busy_1(name_port)      # True  # Không bận
       return com_connecting,busy_gate   #can sua
    
    def  open_config_manual(self,name_port,baudrate):
       com_connecting, busy_gate = self.status_com(name_port)
       debug_print(busy_gate,com_connecting)
       safe_put_queue({
        "type": "software",
        "level": "debug",
        "data": f"Kiểm tra cổng {name_port} — Đang kết nối: {com_connecting}, Bận: {busy_gate}"})
    
       if com_connecting and not busy_gate:
           status_open = self.open_port_setting(name_port,baudrate)
           debug_print("status_open",status_open)
           if status_open:
               data_update = self.to_dict()
               Serial_Com.create_folder.write_json_to_file(Serial_Com.path_folder_config,data_update)
               self.update_data_com()
               debug_print("Mở cổng thành công 1")
               safe_put_queue({
                "type": "software",
                "level": "info",
                "data": f"Mở cổng {name_port} baudrate {baudrate} thành công và lưu cấu hình hệ thống!"})
            
               return True
           else:
               safe_put_queue({
                "type": "software",
                "level": "error",
                "data": f"Không thể mở cổng {name_port} baudrate {baudrate}! Vui lòng kiểm tra thiết bị hoặc kết nối." })
           
               debug_print("Mở cổng khong thành công")
               return False
        
    def is_com_busy_1(self,port_name):
        """Kiem tra xem 1 cong com co ban hay khong"""
        try:
            ser = serial.Serial(port_name)
            ser.close()
            return False  # Cổng rảnh
            
        except serial.SerialException:
            return True  # Cổng bận
    def check_port_exists(self):
        """Kiểm tra cổng COM có còn tồn tại"""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return self.port in ports

    def is_com_busy(self,port_name):
        """Trả về tuple: (exists, busy)
        exists: True nếu cổng còn tồn tại
        busy: True nếu cổng đang bận
        """
        exists = self.check_port_exists()
        if not exists:
            return False, True  # Không tồn tại, coi là bận luôn
        try:
            test_ser = serial.Serial(self.port)
            test_ser.close()
            return True, False  # Tồn tại và không bận
        except serial.SerialException:
            return True, True   # Tồn tại nhưng bận
            
    def check_port(self, name_port: str):
        """Kiểm tra xem cổng có đang được kết nối không"""
        ports = serial.tools.list_ports.comports()
        print("name_port",name_port)
        print("arr_ports",ports)
        for port in ports:
            if port.device == name_port:
                debug_print(f"Tìm thấy cổng: {port.device}")
                return True
        debug_print("Không tìm thấy cổng cần tìm.")
        return False
            
    def show_list_port(self):
        """ trả về mảng các cổng đang kết nối {gate: , description: }"""
        arr_port = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            data = {"gate":port.device,"description":port.description}
            arr_port.append(data)
        debug_print(arr_port)
        return arr_port
    

    def send_data(self, data):
        """Hàm này gửi dữ liệu"""
        if self.ser and self.ser.is_open:
            try:
                data_to_send = f"{data}\n".encode('utf-8')  
                self.ser.write(data_to_send)
                debug_print(f"PC   :{data}")
                # now = time.time()
                # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                # ms = int((now - int(now)) * 1000)
                # debug_print("Thời gian gửi lệnh send trực tiếp",f"{timestamp}.{ms:03d}")
            except serial.SerialException as e:
                debug_print("Lỗi khi gửi dữ liệu: {e}")
        else:
            debug_print("Cổng không tồn tại 2")

    def receive_data(self):
        """Hàm này nhận dữ liệu và trả về data nếu không có lỗi gì"""
        if self.ser and self.ser.is_open:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                debug_print(f"ESP32:{data}")
                # now = time.time()
                # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                # ms = int((now - int(now)) * 1000)
                # debug_print("Thời gian nhận data receive trực tiếp ",f"{timestamp}.{ms:03d}")
                return data
            else:
                return None
        else:
            debug_print("Cổng không tồn tại 3")

    def close_port(self):
        """Hàm này đóng port"""
        if self.ser and self.ser.is_open:
            try: 
                self.ser = None 
                self.port = None        
                self.ser.close()
                debug_print(f"Cổng {self.port} đã được đóng.")
                safe_put_queue({"type":"software","level":"info","data":f"Cổng {self.port} đã được đóng."})
            except serial.SerialException as e:
                debug_print(f"Lỗi khi đóng cổng: {e}")
        else:
            debug_print("Cổng com không tồn tại")
            
    def show_port_info(self):
        """Hàm show thông tin com port"""
        ports = serial.tools.list_ports.comports()
        if not ports:
            debug_print("Không có cổng COM nào được kết nối.")
            return
        debug_print("Danh sách các cổng COM đang kết nối:")
        for port in ports:
            debug_print(f"➤ Tên cổng     : {port.device}")
            debug_print(f"   Mô tả       : {port.description}")
            debug_print(f"   VID:PID     : {port.vid}:{port.pid}")
            debug_print(f"   Tên chip    : {port.name}")
            debug_print(f"   Địa chỉ HW  : {port.hwid}")
            debug_print("-" * 40)

    def to_dict(self):
        """Chuyển object thành dict giống cấu trúc JSON config"""
        return {
            "device_port": self.port,
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "parity": self.parity,
            "stopbits": self.stopbits,
            "timeout": self.timeout,
            "reconnect_interval": self.reconnect_interval
        }
    def update_data_com(self):
        self.Init()


#==================================Hàm chạy kiểm thử====================================================# 
               
# serial_com = Serial_Com()
# serial_com.open_port()

# serial_com = Serial_Com()
# serial_com.open_config_manual("COM3",115200)

# serial_com = Serial_Com()
# serial_com.status_open("COM3",115200)


# serial_com = Serial_Com()
# serial_com.find_port("com3")

# serial_com = Serial_Com()
# serial_com.show_list_port()

