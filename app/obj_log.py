# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Title      : Check OIL bivn / Module put log
# Description: Process put log
# Author     : Vu Vinh Anh
# Email      : anh.vu@example.com
# Created    : 2025-06-30
# Version    : 0.1
# License    : MIT
# -----------------------------------------------------------------------------
import queue
from  shared_queue import queue_log

"""Truyền LLog data có dạng như sau
nếu là log img thì:
    obj_log.safe_put_queue({"type":"image","data":img})
nếu là log excell:
    obj_log.safe_put_queue({"type":"excel","data":[1,2,4,5,5]})
nếu là log in dữ liệu thì:
    safe_put_queue({"type":"software","level":"debug","data":"xin chao ban nhe"})
    safe_put_queue({"type":"software","level":"warning","data":"xin chao ban nhe"})
    safe_put_queue({"type":"software","level":"error","data":"xin chao ban nhe"})
    safe_put_queue({"type":"software","level":"critical","data":"xin chao ban nhe"})
    safe_put_queue({"type":"software","level":"info","data":"xin chao ban nhe"})
"""
ENABLE_PRINT = True # Bật Debug print
def debug_print(*args, **kwargs):
    """In thông tin debug nếu ENABLE_PRINT được bật."""
    if ENABLE_PRINT:
        print(*args, **kwargs) 

def safe_put_queue(data):
    """
    Thêm dữ liệu vào queue một cách an toàn.
    Nếu queue đầy → lấy ra 10 phần tử cũ rồi thêm dữ liệu mới.
    """
    try:
        queue_log.put_nowait(data)
    except queue.Full:
        try:
            # Lấy ra tối đa 10 phần tử cũ
            for _ in range(10):
                queue_log.get_nowait()
            # Sau khi dọn, thêm phần tử mới vào
            queue_log.put_nowait(data)
        except Exception as e:
            debug_print(f"⚠️ Lỗi khi xử lý queue đầy: {e}")
    except Exception as e:
        debug_print(f"⚠️ Lỗi khi ghi vào queue_log: {e}")




  



