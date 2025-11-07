MODE_WAIT_CONNECT = 0
MODE_CONECT =  1
MODE_AUTO =  2

import random
class Manager_STM32:
    def __init__(self):
          self.led_out_red = None
          self.led_out_blue = None
          self.led_out_yellow = None
          self.led_out_btn_reset = None
          self.buzzer_out =  None
          self.btn_inp_start = None 
          self.btn_inp_reset  = None
          self.btn_inp_stop = None
          self.sensor_safety = None
          self.sensor_left_distance = None 
          self.sensor_right_distance = None

        # ====== SET ======
    def set_led_out_red(self, value): self.led_out_red = value
    def set_led_out_blue(self, value): self.led_out_blue = value
    def set_led_out_yellow(self, value): self.led_out_yellow = value
    def set_led_out_btn_reset(self, value): self.led_out_btn_reset = value
    def set_buzzer_out(self, value): self.buzzer_out = value

    def set_btn_inp_start(self, value): self.btn_inp_start = value
    def set_btn_inp_reset(self, value): self.btn_inp_reset = value
    def set_btn_inp_stop(self, value): self.btn_inp_stop = value
    def set_sensor_safety(self, value): self.sensor_safety = value
    def set_sensor_left_distance(self, value): self.sensor_left_distance = value
    def set_sensor_right_distance(self, value): self.sensor_right_distance = value

    # ====== GET ======
    def get_led_out_red(self): return self.led_out_red
    def get_led_out_blue(self): return self.led_out_blue
    def get_led_out_yellow(self): return self.led_out_yellow
    def get_led_out_btn_reset(self): return self.led_out_btn_reset
    def get_buzzer_out(self): return self.buzzer_out

    def get_btn_inp_start(self): return self.btn_inp_start
    def get_btn_inp_reset(self): return self.btn_inp_reset
    def get_btn_inp_stop(self): return self.btn_inp_stop
    def get_sensor_safety(self): return self.sensor_safety
    def get_sensor_left_distance(self): return self.sensor_left_distance
    def get_sensor_right_distance(self): return self.sensor_right_distance
    
    def update_status_from_string(self,data: str):
        """
        hàm này cần chạy khi bắt đầu kết nối để update được trạng thái nút nhấn luôn
        data: chuỗi dạng '#status_all:1,0,1,1,0,0,1,0,0,1,1\n'
        """
        try:
            if not data.startswith("status_all:"):
                return  # Không phải chuỗi trạng thái hợp lệ
            raw_values = data.replace("status_all:", "").strip()

            values = list(map(int, raw_values.split(",")))

            if len(values) < 11:
                print("⚠️ Dữ liệu không đủ số trạng thái:", values)
                return

            (self.led_out_yellow,
             self.led_out_red,
             self.led_out_blue,
             self.buzzer_out,
             self.led_out_btn_reset,
             self.btn_inp_reset,
             self.btn_inp_stop,
             self.btn_inp_start,
             self.sensor_left_distance,  
             self.sensor_right_distance,
             self.sensor_safety, 
             ) = values[:11]

            print("✅ Cập nhật trạng thái thành công:")
            print(self.__dict__)

        except Exception as e:
            print("❌ Lỗi khi parse chuỗi:", e)
    def check_stop(self):
        
    

  
    
        

    





















    def init(self, mode="random"):
        """Khởi tạo các trạng thái 0/1"""
        if mode == "random":
            self.led_out_red = random.randint(0, 1)
            self.led_out_blue = random.randint(0, 1)
            self.led_out_yellow = random.randint(0, 1)
            self.led_out_btn_reset = random.randint(0, 1)
            self.btn_inp_start = random.randint(0, 1)
            self.btn_inp_reset = random.randint(0, 1)
            self.btn_inp_stop = random.randint(0, 1)
            self.sensor_safety = random.randint(0, 1)
            self.sensor_left_distance = random.randint(0, 1)
            self.sensor_right_distance = random.randint(0, 1)
        else:
            # Mode default = 0/1 cố định
            self.led_out_red = 0
            self.led_out_blue = 0
            self.led_out_yellow = 0
            self.led_out_btn_reset = 0
            self.btn_inp_start = 0
            self.btn_inp_reset = 0
            self.btn_inp_stop = 0
            self.sensor_safety = 1
            self.sensor_left_distance = 0
            self.sensor_right_distance = 0
        

    def show_all(self):
        """Hiển thị toàn bộ trạng thái hiện tại"""
        print("📟 Trạng thái hiện tại của STM32:")
        for k, v in self.__dict__.items():
            if k != "obj_send":
                print(f"  {k:25}: {v}")

        print("✅ Các tín hiệu STM32 đã khởi tạo mặc định (0/1):")
        for k, v in self.__dict__.items():
            if k != "obj_send":
                print(f"  {k:25}: {v}")
    def set_output_all(self, red=None, blue=None, yellow=None, btn_reset=None, buzzer=None):
            """
            Set trạng thái cho 5 output. 
            Truyền None để giữ nguyên, 0 hoặc 1 để thay đổi.
            """
            if red is not None:
                self.led_out_red = red
            if blue is not None:
                self.led_out_blue = blue
            if yellow is not None:
                self.led_out_yellow = yellow
            if btn_reset is not None:
                self.led_out_btn_reset = btn_reset
            if buzzer is not None:
                self.buzzer_ou = buzzer




# def emergency_stop(self):
stm32 = Manager_STM32()

stm32.update_status_from_string("status_all:1,0,1,1,0,0,1,0,0,1,1")
stm32.show_all()

        
         
    