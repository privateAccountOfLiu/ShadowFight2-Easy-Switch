import os
import sys
import time
from pathlib import Path
from typing import List


def write_to_log(msg: str | List[str]) -> None:
    """Append a timestamped log message or a list of messages to log.txt."""
    time_msg = time.strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))
    with open("./log.txt", "a") as log:
        if isinstance(msg, list):
            log.writelines([f"{time_msg}: {i}\n" for i in msg])
        elif isinstance(msg, str):
            log.write(f"{time_msg}: {msg}\n")
        else:
            log.write(f"{time_msg}: Log Error!\n")


def get_dir(path: str) -> str:
    """Resolve a resource path correctly in both frozen and non-frozen environments."""
    write_to_log(f"[Load Resource: {path}]: {sys.path}\n{sys.argv}\n{Path(sys.executable).parent}")
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(sys.executable).parent
    else:
        base_path = Path(os.path.abspath("."))
    return str(base_path / path)


def get_error_msg(error: Exception) -> str:
    """Build a detailed multi-line error message for logging and dialogs."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return (
        f"\n"
        f"Error Msg: {error} !\n"
        f"Error Type: {exc_type.__name__}\n"
        f"Detail: {exc_value}\n"
        f"File: {exc_traceback.tb_frame.f_code.co_filename}\n"
        f"Line: {exc_traceback.tb_lineno}\n"
        f"Function: {exc_traceback.tb_frame.f_code.co_name}\n"
    )


def make_dir() -> None:
    """Ensure basic working directories for animation, csv and model outputs exist."""
    _dirs = ["./animation", "./csv", "./model"]
    for d in _dirs:
        if not os.path.exists(d):
            os.mkdir(d)


def find_regular_files(regulation, filepath) -> int:
    """Count files in a directory whose names end with any suffix from regulation."""
    return sum(any(filename.lower().endswith(i) for i in regulation) for filename in os.listdir(filepath))
