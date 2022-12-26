"""Create a High Resolution Screenshot and sends it to RV."""
import os
import threading
import time
from datetime import datetime
from subprocess import PIPE, Popen

import unreal

RVPUSH = os.environ.get(
    "RVPUSH", r"C:\Program Files\ShotGrid\RV-2022.3.1\bin\rvpush.exe"
)


def create_screenshot() -> str:
    """Create a high res screenshot of current viewport.

    :return: path to the screenshot
    :rtype: str
    """
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    screenshot_dir = os.path.abspath(unreal.Paths.screen_shot_dir())
    screenshot_filename = "screenshot_{0}.png".format(now)
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, screenshot_filename)

    return screenshot_path


def push2rv(file_path: str) -> bool:
    """Push the screenshot to current RV session.

    Using rvpush.exe, it will try to push the image to an active RV
    session tagged "unreal". If it can't find one, it will create a new session.
    (Because the screenshot will be done after the python process, we need to run this
    function in a different thread. )

    :param file_path: file path to the image
    :type file_path: str
    :return: False if it couldn't find the file after 10sec.
    :rtype: bool
    """
    s = time.time()
    while True:
        if os.path.exists(file_path):
            break
        elapsed = time.time() - s
        if elapsed > 10:
            return False
        time.sleep(1)

    # rvpush commandline
    cmd = [RVPUSH, "-tag", "unreal", "merge", "[", file_path, "]"]
    Popen(cmd, stdout=PIPE)

    return True


def ue2rv() -> None:
    """Send screenshot to RV."""
    path = create_screenshot()
    # couldn't find a way to wait for the screenshot, so checking for it
    # in another thread.
    rv = threading.Thread(target=push2rv, args=(path,))
    rv.start()
