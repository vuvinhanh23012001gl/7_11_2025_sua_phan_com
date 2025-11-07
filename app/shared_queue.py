# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module Queue
# Description: Create Queue 
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
import queue
SIZE_QUEUE_RX_WEB_API = 50
SIZE_QUEUE_TX_WEB_LOG = 50
SIZE_QUEUE_TX_WEB_MAIN = 50
SIZE_QUEUE_ACCEPT_CAPTURE =  50
SIZE_QUEUE_CAPTURE_DETECT =  50
SIZE_QUEUE_RX_ARM = 50
SIZE_QUEUE_TX_ARM = 50
SIZE_QUEUE_LOG = 500 # img , excell , txt

queue_accept_capture = queue.Queue(maxsize = SIZE_QUEUE_ACCEPT_CAPTURE) # Queue này chịu chấp nhận lệnh từ hàm func và đọc queue này để nhận lệnh chụp ảnh
queue_rx_web_api = queue.Queue(maxsize=SIZE_QUEUE_RX_WEB_API)     # Queue này chịu chấp nhận dữ liệu để tiến hành chạy nhiều điểm
queue_tx_web_log = queue.Queue(maxsize=SIZE_QUEUE_TX_WEB_LOG)     # Queue này để tổng hợp dữ liệu log gửi lên client
queue_tx_web_main = queue.Queue(maxsize=SIZE_QUEUE_TX_WEB_MAIN)   # Queue này để gửi dữ liệu ảnh và data phán định
queue_process_capture_detect = queue.Queue(maxsize = SIZE_QUEUE_CAPTURE_DETECT) # Queue nhận ảnh để phán định
queue_tx_arm = queue.Queue(maxsize = SIZE_QUEUE_TX_ARM)           # Queue gửi tín hiệu ARM
queue_rx_arm = queue.Queue(maxsize = SIZE_QUEUE_RX_ARM)           # Queue nhận tín hiệu ARM
queue_log = queue.Queue(maxsize = SIZE_QUEUE_LOG)                 # Queue lưu log hình ảnh excell log phán định