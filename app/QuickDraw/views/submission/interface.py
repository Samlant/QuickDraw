from QuickDraw.views.submission.base.properties import ViewInterface
from QuickDraw.views.submission.dirs.tab import make_dirs_widgets
from QuickDraw.views.submission.email.tab import make_email_widgets
from QuickDraw.views.submission.home.tab import make_home_widgets
from QuickDraw.views.submission.quoteforms.registrations.tab import (
    make_quoteform_widgets,
)
from QuickDraw.views.submission.templates.tab import make_templates_widgets
from QuickDraw.views.submission.base.protocols import Presenter


class MainWindow(ViewInterface):
    def __init__(
        self,
        icon_src: str,
    ):
        super().__init__(
            icon_src,
        )

    def create_UI_obj(
        self,
        presenter: Presenter,
        view_palette,
    ):
        """This creates the GUI root,  along with the main
        functions to create the widgets.
        """
        self.assign_interpreter(view_palette)
        self.assign_private_string_bool_vars()
        self.assign_window_traits()
        self.create_notebook()
        # Can we loop this next method?
        self.create_tabs()
        # Separate each tab into their respective module
        make_home_widgets(self, presenter, self.palette)
        make_templates_widgets(self, presenter, self.palette)
        make_email_widgets(self, presenter, self.palette)
        make_dirs_widgets(self, presenter, self.palette)
        make_quoteform_widgets(self, presenter, self.palette)

    def save_settings(self, page: str, data: dict[str, any]):
        if page == "dirs":
            self.watch_dir