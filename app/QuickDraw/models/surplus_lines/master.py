import os
import subprocess
import sys
from win10toast import ToastNotifier
import logging.config

from model.surplus_lines.dev.logs import LOGGING_CONFIG
from model.surplus_lines.surplus_lines.automation import Automator
from model.surplus_lines.dev import exceptions

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger(__name__)


class SurplusLinesAutomator:
    def __init__(self, config_worker):
        self.config_worker = config_worker

    def start(self):
        app = Automator(self.config_worker)
        app.spawn_window()
        if not app.exited:
            try:
                app.parse_doc()
                stamp_num = 1
                stamp_paths = []
                for payload in app.payloads:
                    log.debug(
                        msg="Current payload: {0}".format(payload),
                    )
                    log.info(
                        msg="Performing the web call.",
                    )
                    form_data = app.perform_web_call(payload)
                    log.info(
                        msg="Secured the response and formatted it.",
                    )
                    log.debug(
                        msg="The formatted response is: {0}.".format(form_data),
                    )
                    stamp_paths.append(app.fill_docs(form_data, stamp_num))
                    stamp_num += 1
            except exceptions.DocError:
                sys.exit(1)
            except Exception as e:
                print(str(e))
                sys.exit(1)
            else:
                log.info(
                    msg="Combining stamps into your document.",
                )
                new_file_path = app.combine_docs(stamp_paths)
                log.info(
                    msg="Stamps combined. The stamped file location is: {0}.".format(
                        new_file_path
                    ),
                )
                file_browser_path = os.path.join(os.getenv("WINDIR"), "explorer.exe")
                log.info(
                    msg="Opening a file window to show you the new, stamped file.  The file will be highlighted for your convenience.",
                )
                log.debug(
                    msg="File Explorer path used: {0}.".format(file_browser_path),
                )
                subprocess.run([file_browser_path, "/select,", new_file_path])
                log.debug(
                    msg="Initializing and showing notification box via ToastNotifier.",
                )
                toaster = ToastNotifier()
                toaster.show_toast(
                    "SUCCESS! Your doc is now stamped.",
                    "A new window will show you the finished file.",
                    duration=5,
                )
