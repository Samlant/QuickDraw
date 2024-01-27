from typing import Protocol

from QuickDraw.views.submission import base
from QuickDraw.views.submission.dirs.tab import make_dirs_widgets
from QuickDraw.views.submission.email.tab import make_email_widgets
from QuickDraw.views.submission.home.tab import make_home_widgets
from QuickDraw.views.submission.quoteforms.registrations.tab import (
    make_quoteform_widgets,
)
from QuickDraw.views.submission.templates.tab import make_templates_widgets
from QuickDraw.views.themes import palettes
from QuickDraw.views.themes.applicator import create_style
from QuickDraw.helper import open_config

# Create a style for the application using the selected palette
PALETTE = palettes.BlueRose()


class Presenter(Protocol):
    ...


class MainWindow(base.MainWindow):
    def __init__(self, icon_src: str):
        super().__init__(
            icon_src,
        )

    def create_UI_obj(self, presenter: Presenter):
        """This creates the GUI root,  along with the main
        functions to create the widgets.
        """
        style = create_style(self.root, PALETTE)
        self.assign_style(style)
        self.assign_private_string_bool_vars()
        self.assign_window_traits()
        self.create_notebook()
        # Can we loop this next method?
        self.create_tabs()
        # Separate each tab into their respective module
        make_home_widgets(self, presenter, PALETTE)
        make_templates_widgets(self, presenter, PALETTE)
        make_email_widgets(self, presenter, PALETTE)
        make_dirs_widgets(self, presenter, PALETTE)
        make_quoteform_widgets(self, presenter, PALETTE)

    def save_settings(self, page: str, data: dict[str, any]):
        if page == "dirs":
            self.watch_dir
