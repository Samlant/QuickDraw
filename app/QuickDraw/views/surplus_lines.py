import logging
from tkinter import ttk, Text, filedialog, Toplevel
from typing import Protocol

from tkinterdnd2 import DND_FILES, TkinterDnD

from QuickDraw.views.themes.applicator import create_style


class Presenter(Protocol):
    def process_SL_doc(self, event):
        ...
    
    def save_sl_output_dir(self, event):
        ...


log = logging.getLogger(__name__)


class SurplusLinesView:
    def __init__(self):
        self.root: TkinterDnD = None
        self.style  = None
        self.palette = None

    @property
    def output_dir(self) -> str:
        self._output_dir.get("1.0", "end-1c")

    @output_dir.setter
    def output_dir(self, new_output_dir) -> None:
        del self.output_dir
        self._output_dir.insert("1.0", new_output_dir)

    @output_dir.deleter
    def output_dir(self) -> None:
        self._output_dir.delete("1.0", "end")

    @property
    def doc_path(self) -> str:
        self._doc_path.get("1.0", "end-1c")

    @doc_path.setter
    def doc_path(self, new_doc_path) -> None:
        del self._doc_path
        self._doc_path.insert("1.0", new_doc_path)

    @doc_path.deleter
    def doc_path(self) -> None:
        self._doc_path.delete("1.0", "end")

    def make_view(
        self,
        presenter,
        view_palette,
        output_dir: str | None,
    ):
        if not self.root:
            self.root = TkinterDnD.Tk()
            self.style = create_style(self.root, view_palette)
            self.palette = view_palette
            self._assign_window_traits()
            self._create_widgets(presenter)
            if output_dir:
                self.output_dir = output_dir
            self.root.mainloop()
        else:
            try:
                self.root = TkinterDnD.Tk()
            except:
                pass
            finally:
                self.root.iconify()
        # self.root.mainloop()
                
    def on_close(self):
        print('destroying window')
        self.root.destroy()
        self.root = None

    def _assign_window_traits(self):
        self.root.geometry("730x250")
        self.root.configure(background="#5F9EA0")
        self.root.attributes("-topmost", True)
        self.root.title("FSL AutoFiller")
        self.root.attributes("-alpha", 0.95)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        log.debug(
            msg="Window attributes are set., creating frames for UI.",
        )

    def _create_widgets(self, presenter: Presenter):
        log.debug(
            msg="Creating widgets for SL UI.",
        )
        top = ttk.Frame(self.root)
        top.pack(
            fill="x",
            expand=False,
            side="top",
            padx=3,
            pady=(5, 0),
        )
        middle1 = ttk.Frame(self.root)
        middle1.pack(
            fill="both",
            expand=False,
            side="top",
            padx=3,
        )
        middle2 = ttk.Frame(self.root)
        middle2.pack(
            fill="both",
            expand=True,
            side="top",
            padx=3,
            pady=(4, 0),
        )
        bottom = ttk.Frame(self.root)
        bottom.pack(
            fill="both",
            expand=True,
            side="top",
            padx=3,
            pady=3,
        )
        log.debug(
            msg="Created frames for UI, setting labels",
        )
        ttk.Label(
            top,
            text="FIRST TIME USERS!",
            font=("Times New Roman", 14, "bold"),
        ).pack(side="left", anchor="se")
        ttk.Label(
            middle1,
            text="↪",
            font=("Times New Roman", 30, "bold"),
        ).pack(side="left")
        ttk.Label(
            middle1,
            text="Choose save location for the stamped doc:",
        ).pack(side="left")
        ttk.Label(
            middle2,
            text="Drag-N-Drop your document below!",
            font=("Times New Roman", 18, "bold"),
        ).pack(
            side="top",
        )
        log.debug(
            msg="Created labels for UI, creating button.",
        )
        ttk.Button(
            middle1,
            command=lambda: self._browse_output_dir(presenter=presenter),
            text="Browse",
        ).pack(
            side="left",
            padx=3,
            pady=3,
        )
        log.debug(
            msg="Created button for UI, creating drag-n-drop Text box.",
        )
        self._output_dir = Text(
            master=middle1,
            foreground=self.palette.alt_fg_color,
            background=self.palette.alt_bg_color,
            highlightcolor=self.palette.alt_bg_color,
            selectbackground=self.palette.alt_fg_color,
            selectforeground=self.palette.alt_bg_color,
            height=2,
            width=48,
        )
        self._output_dir.pack(
            side="left",
            padx=3,
            ipady=0,
        )

        self._doc_path = Text(
            bottom,
            foreground=self.palette.alt_fg_color,
            background=self.palette.alt_bg_color,
            highlightcolor=self.palette.alt_bg_color,
            selectbackground=self.palette.alt_fg_color,
            selectforeground=self.palette.alt_bg_color,
            name="user_doc_path",
        )
        self._doc_path.drop_target_register(DND_FILES)
        self._doc_path.dnd_bind(
            "<<Drop>>",
            presenter.process_SL_doc,
        )
        self._doc_path.pack(
            fill="both",
            expand=True,
            ipady=5,
        )
        log.debug(
            msg="Created and activated drag-n-drop for Text box.",
        )

    def _browse_output_dir(self, presenter: Presenter):
        try:
            _dir = filedialog.askdirectory(mustexist=True)
        except AttributeError as e:
            log.info(
                msg="The Folder Browser window must have been closed before user clicked 'OK'. Continuing on.",
            )
            log.debug(
                msg=f"Caught {e}, continuing on.",
            )
        else:
            presenter.save_sl_output_dir(_dir)
