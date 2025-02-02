from messages import nanos
from frame import capture, live
import logging
from multiprocessing import Process


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("AthenaUnified"),
    logging.StreamHandler()
])



if __name__ == "__main__":
    live_caputre_send = live.LiveCaptureSend()
    cv_proc = Process(target=live_caputre_send.main_loop_runner)
    cv_proc.start()
    cv_proc.join()
