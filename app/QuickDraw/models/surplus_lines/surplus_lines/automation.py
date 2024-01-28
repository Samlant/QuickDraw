from dataclasses import dataclass
from pathlib import Path
import logging

from Quickdraw.helper import open_config
from model.surplus_lines.dev import exceptions
from model.surplus_lines.surplus_lines.carriers.base import Carrier
from model.surplus_lines.surplus_lines.doc.filler import DocFiller
from model.surplus_lines.surplus_lines.doc.parser import DocParser
from model.surplus_lines.surplus_lines.web.scraper import Driver, Response


log = logging.getLogger(__name__)


@dataclass
class Payload:
    """Holds data to be inputted into the FSL website"""

    policy_num: str | int
    premium: float
    eff_date: str
    transaction_type: int | str
    

    def __post_init__(self):
        # static vars below:
        self.coverage_code: int | str = "3006"
        self.tax_status: int | str = "0"
        self.policy_fee: int = 0
        self.uri: str = "https://www.fslso.com/tax-estimator"


class Automator:
    def __init__(self, config_worker):
        self.root: TkinterDnD.Tk = None
        self.user_doc_path: Path = None
        self.payloads: list[Payload] = []
        self.form_data: dict[str, float | str] = None
        self.exited: bool = False
        self.carrier_obj: Carrier = None
        self.stamps: list[Path] = []
        self.doc_filler: DocFiller = None
        self.config = config_worker
    
    @property
    def output_dir(self) -> str:
        "TODO DOUBLE CHECK!"
        config = open_config()
        value = config.get(
            "Surplus lines settings",
            "output_save_dir",
        )
        return value[1].value


    def _save_user_doc_path(self, event):
        log.info(msg="Saving the PDF's path.")
        log.debug(
            msg="Event data: {0}".format(event.data),
        )
        if not self.output_dir:
            log.info(
                msg="The output folder isn't set. This needs to be set before proceeding with the program. ",
            )
            exceptions.spawn_message(
                "Warning",
                """Please choose a folder to save the final, stamped file
                in first. Click 'OK' here first, then click the 'Browse' button to select your desired folder.""",
                0x10 | 0x0,
            )
        else:
            self.user_doc_path = Path(event.data.strip("{}")).resolve()
            self.exited = False
            log.info(
                msg="Saved the PDF's path. Destroying the UI window.",
            )
            log.debug(
                msg="The PDF path is: {0}".format(self.user_doc_path),
            )
            self.root.destroy()

    def browse_output_path(self):
        try:
            dir_path = filedialog.askdirectory(mustexist=True)
            self.output_path.delete("1.0", END)
            self.output_path.insert("1.0", dir_path)
            self.config.handle_save_contents(
                "Surplus lines settings", {"output_save_dir": dir_path}
            )
            # set_key(ENV_PATH, "OUTPUT_DIR", dir_path)
        except AttributeError as e:
            log.info(
                msg="The Folder Browser window must have been closed before user clicked 'OK'. Continuing on.",
            )
            log.debug(
                msg="Caught {0}, continuing on.".format(e),
            )

    def spawn_window(self):
        self.root = TkinterDnD.Tk()
        self.root.geometry("730x250")
        self.root.configure(background="#5F9EA0")
        self.root.attributes("-topmost", True)
        self.root.title("FSL AutoFiller")
        self.root.attributes("-alpha", 0.95)
        log.debug(
            msg="Set window attributes, creating frames for UI.",
        )
        self.root.top = Frame(self.root)
        self.root.top.pack(
            fill=X,
            expand=False,
            side=TOP,
            padx=3,
            pady=(5, 0),
        )
        self.root.middle1 = Frame(self.root)
        self.root.middle1.pack(
            fill=BOTH,
            expand=False,
            side=TOP,
            padx=3,
        )
        self.root.middle2 = Frame(self.root)
        self.root.middle2.pack(
            fill=BOTH,
            expand=True,
            side=TOP,
            padx=3,
            pady=(4, 0),
        )
        self.root.bottom = Frame(self.root)
        self.root.bottom.pack(
            fill=BOTH,
            expand=True,
            side=TOP,
            padx=3,
            pady=3,
        )
        log.debug(
            msg="Created frames for UI, setting labels",
        )
        Label(
            self.root.top,
            text="FIRST TIME USERS!",
            font=("Times New Roman", 14, "bold"),
        ).pack(side=LEFT, anchor="se")
        Label(
            self.root.middle1,
            text="↪",
            font=("Times New Roman", 30, "bold"),
        ).pack(side=LEFT)
        Label(self.root.middle1, text="Choose save location for the stamped doc:").pack(
            side=LEFT
        )
        Label(
            self.root.middle2,
            text="Drag-N-Drop your document below!",
            font=("Times New Roman", 18, "bold"),
        ).pack(
            side=TOP,
        )
        log.debug(
            msg="Created labels for UI, creating button.",
        )
        Button(
            self.root.middle1,
            command=self.browse_output_path,
            text="Browse",
        ).pack(
            side=LEFT,
            padx=3,
            pady=3,
        )
        log.debug(
            msg="Created button for UI, creating drag-n-drop Text box.",
        )
        self.output_path = Text(
            self.root.middle1,
            height=1,
            width=48,
        )
        self.output_path.pack(
            side=LEFT,
            padx=3,
            ipady=4,
        )

        self.root.doc_box = Text(
            self.root.bottom,
            background="#59f3e3",
            name="user_doc_path",
        )
        self.root.doc_box.drop_target_register(DND_FILES)
        self.root.doc_box.dnd_bind(
            "<<Drop>>",
            self._save_user_doc_path,
        )
        self.root.doc_box.pack(
            fill=BOTH,
            # anchor=NSEW,
            expand=True,
            ipady=5,
        )
        log.debug(
            msg="Created and activated drag-n-drop for Text box.",
        )
        if self.output_dir:
            log.debug(
                msg="output_dir detected, prefilling Text box with its path: {0}".format(
                    self.output_dir
                ),
            )
            self.output_path.insert("1.0", self.output_dir)
        else:
            log.info(
                msg="No output folder selected.  Please choose a folder to save the finalized, stamped file in before dragging a PDF file onto the window.",
            )
        log.debug(
            msg="Spawning window, starting mainloop.",
        )
        self.root.mainloop()

    def parse_doc(self):
        """Saves premium & eff date into a Payload object."""
        log.debug(
            msg="Initializing DocParser class with user doc path: {0}.".format(
                self.user_doc_path
            ),
        )
        try:
            dp = DocParser(self.user_doc_path)
        except exceptions.UnknownDocType as UDT:
            exceptions.spawn_message("Error", str(UDT), 0x10 | 0x0)
            # btn = OK
            # exit SL window and terminate thread
            log.warning(
                msg="{0}".format(str(UDT)),
                exc_info=1,
            )
            self.root.destroy()
            raise exceptions.DocError(self.user_doc_path) from UDT
        try:
            carrier_builder, trans_type = dp.build_market_class(self.user_doc_path)
        except exceptions.DocParseError as DPE:
            log.warning(
                msg=str(DPE),
            )
            output = exceptions.spawn_message("Error", str(DPE), 5)
            if output == 4:
                # btn = retry
                self.restart_GUI()
                log.info(
                    msg="User decided to restart and try again.",
                    exc_info=1,
                )
            else:
                # btn = cancel
                # exit SL window and terminate thread
                log.info(
                    msg="User decided to cancel instead of trying again. Exiting.",
                    exc_info=1,
                )
                raise exceptions.DocError(self.user_doc_path) from DPE
        except exceptions.UnsupportedDocType as UDT:
            output = exceptions.spawn_message("Error", str(UDT), 5)
            if output == 4:
                # btn = retry
                log.info(
                    msg="User decided to restart and try again.",
                    exc_info=1,
                )
                self.restart_GUI()
            else:
                # btn = cancel
                # exit SL window and terminate thread
                log.info(
                    msg="User decided to cancel instead of trying again. Exiting.",
                    exc_info=1,
                )
                self.root.destroy()
                raise exceptions.DocError(self.user_doc_path) from UDT
        except exceptions.UnknownDocType as UDT:
            exceptions.spawn_message("Error", str(UDT), 0x10 | 0x0)
            # btn = OK
            # exit SL window and terminate thread
            log.warning(
                msg="{0}".format(str(UDT)),
                exc_info=1,
            )
            self.root.destroy()
            raise exceptions.DocError(self.user_doc_path) from UDT
        except exceptions.SurplusLinesNotApplicable as SLNA:
            exceptions.spawn_message("Error", str(SLNA), 0x10 | 0x0)
            # btn = OK
            # exit SL window and terminate thread
            log.warning(
                msg="{0}".format(str(SLNA)),
                exc_info=1,
            )
            self.root.destroy()
            raise exceptions.DocError(self.user_doc_path) from SLNA
        else:
            log.debug(
                msg="Starting to build carrier object using the CarrierBuilder.",
            )
            self.carrier_obj = carrier_builder.build(self.user_doc_path)
            for premium, policy_num in zip(
                self.carrier_obj.premiums, self.carrier_obj.policy_nums
            ):
                log.debug(
                    msg="Zipping together the premiums and policy nums, then iterating over them to add to the payload object.",
                )
                log.debug(
                    msg="Current Premium: {0}. Current Policy Num: {1}".format(
                        premium, policy_num
                    ),
                )
                payload = Payload(
                        policy_num=policy_num,
                        premium=premium,
                        eff_date=self.carrier_obj.eff_date,
                        transaction_type=trans_type,
                    )
                self.payloads.append(payload
                )
            log.debug(
                msg="The finalized payload object is: {0}".format(self.payloads),
            )

    def perform_web_call(self, payload: Payload) -> dict[str, float | str]:
        log.info(
            msg="Initializing the web driver.",
        )
        driver = Driver()
        log.info(
            msg="Sending the web call loaded with the payload from the PDF file.",
        )
        driver.send_call(payload)
        log.info(
            msg="Getting the response.",
        )
        response = self._get_response(driver)
        return self._format_response(response, payload)

    def _get_response(self, driver: Driver) -> Response:
        response: Response = driver.get_response()
        return response

    def _format_response(
        self,
        response: Response,
        payload: Payload,
    ) -> dict[str, float | str]:
        form_data = {
            "tax": "",
            "service_fee": "",
            "subtotal_fees": "",
            "total_cost": "",
        }
        for key, value in response.get_dict().items():
            x = value.replace("$", "").replace(",", "")
            if "(" in x:
                y = float(x.replace("(", "").replace(")", ""))
                x = -abs(y)
            form_data[key] = "{:,.2f}".format(float(x))
        return self.__data_to_dict(form_data, payload)

    def __data_to_dict(
        self,
        form_data: dict,
        payload: Payload,
    ) -> dict[str, float | str]:
        other_data = {
            "insured_name": self.carrier_obj.client_name,
            "policy_num": payload.policy_num,
            "premium": "{:,.2f}".format(payload.premium),
            "policy_fee": "{:,.2f}".format(payload.policy_fee),
            "eff_from": self.carrier_obj.eff_date,
            "eff_to": self.carrier_obj.exp_date,
        }
        form_data.update(other_data)
        return form_data

    def fill_docs(self, form_data: dict[str, float | str], stamp_num: int) -> Path:
        log.debug(
            msg="Initializing DocFiller class. Processing doc with stamp number: {0}".format(
                stamp_num
            ),
        )
        doc_filler = DocFiller(self.output_dir)
        stamp_path = doc_filler.process_doc(form_data, stamp_num)
        return stamp_path

    def combine_docs(self, stamps: list[Path]):
        doc_filler = DocFiller(self.output_dir)
        log.debug(
            msg="Using these stamps: {0}, and inserting into page index: {1}, inside user doc path: {2}".format(
                stamps, self.user_doc_path, self.carrier_obj.insert_page_index
            ),
        )
        new_path = doc_filler.combine_stamps_into_pdf(
            self.user_doc_path,
            stamps,
            self.carrier_obj.insert_page_index,
        )
        return new_path

    def restart_GUI(self):
        self.market = None
        self.spawn_window()
