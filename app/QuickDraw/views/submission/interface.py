from typing import Protocol
from QuickDraw.views.submission import base
from QuickDraw.views.themes import palettes
from QuickDraw.views.themes.applicator import create_style
from QuickDraw.views.submission.home.tab import make_home_widgets
from QuickDraw.views.submission.templates.tab import make_templates_widgets
from QuickDraw.views.submission.email.tab import make_email_widgets
from QuickDraw.views.submission.dirs.tab import make_dirs_widgets
from QuickDraw.views.submission.quoteforms.registrations.tab import (
    make_quoteform_widgets,
)


PALETTE = palettes.BlueRose()


class Presenter(Protocol):
    ...


##################################
# CHANGE TAB PROPERTY FROM SELF.<TAB NAME> TO SELF.TABS.<SHORTENED TAB NAME>
##################################


class MainWindow(base.Submission):
    def __init__(self, positive_value, negative_value, icon_src: str):
        style = create_style(self, PALETTE)
        super().__init__(
            positive_value,
            negative_value,
            icon_src,
            style,
        )

    def create_UI_obj(self, presenter: Presenter):
        """This creates the GUI root,  along with the main
        functions to create the widgets.
        """
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
