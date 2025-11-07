# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn /Module Value common
# Description:  Value common
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
#file này để lưu những giá trị chung được sử dụng trong toàn bộ phần mềm
import threading
click_page_html = threading.Lock()              
click_page_html = 0
the_first_connect = True    
is_run = 0
status_check_connect_arm = False
status_check_connect_camera = False
mumber_total_product = 0   #run dung
mumber_product_oke = 0  #run dung
NAME_FILE_CHOOSE_MASTER = "choose_master"
NAME_FILE_STATIC = "static"
NAME_FOLDER_CONFIG = "config"
NAME_FILE_IMG_RETRAINING = "Product_Img_Retraining"
NAME_FOLDER_LOG = "log"
NAME_FOLDER_USER = "user"


