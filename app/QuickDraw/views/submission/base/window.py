from tkinter import ttk, filedialog, StringVar, BooleanVar, Toplevel, Frame

from tkinterdnd2 import TkinterDnD

from QuickDraw.helper import AVAILABLE_CARRIERS
from QuickDraw.views.submission.helper import ALL_TABS
from QuickDraw.views.themes.applicator import create_style


class Window:
    def __init__(
        self,
        icon_src: str,
    ) -> None:
        self.icon = icon_src

    def assign_interpreter(
        self,
        view_palette,
    ):
        self.root = TkinterDnD.Tk()
        self.style = create_style(self.root, view_palette)
        self.palette = view_palette

    def assign_private_string_bool_vars(self) -> None:
        """Assigns tkinter-specific attributes so that the getters /
        setters work and other modules do not need to need tkinter.
        """
        for vars_and_types in ALL_TABS.values():
            for var, var_type in vars_and_types.items():
                if var_type == "text":
                    continue
                elif var_type == "str":
                    setattr(
                        self,
                        "_" + var,
                        StringVar(self.root, "", var),
                    )
                elif var_type == "bool":
                    setattr(
                        self,
                        "_" + var,
                        BooleanVar(self.root, False, var),
                    )

        for carrier in AVAILABLE_CARRIERS:
            var = BooleanVar(
                self.root,
                False,
                carrier.name,
            )
            setattr(self, "_" + carrier.name, var),

    def assign_window_traits(self):
        self.root.geometry("760x600")
        # self.root.configure(background="red")
        self.root.attributes("-topmost", True)
        self.root.title("QuickDraw")
        self.root.attributes("-alpha", 0.95)
        self.root.iconbitmap(self.icon)

    def create_notebook(self):
        self.tabs = ttk.Notebook(master=self.root)
        self.tabs.pack(fill="both", pady=0, expand=True)

    def create_tabs(self):
        self.tabs.home = ttk.Frame(self.tabs)
        self.tabs.templates = ttk.Frame(self.tabs)
        self.tabs.email = ttk.Frame(self.tabs)
        self.tabs.dirs = ttk.Frame(self.tabs)
        self.tabs.quoteforms = ttk.Frame(self.tabs)
        self.tabs.add(self.tabs.home, text="Home - Outbox")
        self.tabs.add(self.tabs.templates, text="Email Templates")
        self.tabs.add(self.tabs.email, text="Email Settings")
        self.tabs.add(self.tabs.dirs, text="Folder Settings")
        self.tabs.add(self.tabs.quoteforms, text="Quoteform Registrations")

    def _browse_qf_path(self, event: None):
        if event:
            print(event.data)
        try:
            dir_name = filedialog.askopenfilename()
            if not dir_name == "":
                self.quoteform = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_extra_file_path(self):
        try:
            dir_name = filedialog.askopenfilename()
            if dir_name != "":
                self.attachments = self.dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def get_active_focus(self) -> dict:
        return self.root.focus_get()

    def _browse_watch_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.watch_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_new_biz_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.new_biz_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_renewals_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.renewals_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _add_custom_parent_dir(self):
        dir_name: str | int = self.custom_parent_dir
        self._insert_row(data=dir_name)
        del self.custom_parent_dir

    def _add_custom_sub_dir(self):
        # Get selected row_id
        current_selected_id = self.tree_dir.selection()
        parent_name = self.tree_dir.set(current_selected_id)["1"]
        dir_name: str | int = self.custom_sub_dir
        self.tree_dir.insert(
            parent=current_selected_id,
            index="end",
            text=parent_name,
            values=dir_name,
            open=True,
        )
        del self.custom_sub_dir

    def _insert_row(self, data: str):
        if isinstance(data, int):
            data = str(data)
        if "/" in data:
            # split "/" up into a list of strings
            entry_list = data.split("/")
            # find the top-most parent's row id by name & label == "Top Level"
            parent_id = self.__find_row_id_by_name(entry_list[0])
            # check for any other slashes / parents
            if len(entry_list) == 3:
                # find the next parent's row id by name & label != "Top Level"
                sub_parent_id = self.__find_row_id_by_name(entry_list[1])
                # create row under sub_parent row:
                self.tree_dir.insert(
                    parent=sub_parent_id,
                    index="end",
                    text=entry_list[1],
                    values=entry_list[2],
                    open=True,
                )
            else:
                # create row under parent row:
                self.tree_dir.insert(
                    parent=parent_id,
                    index="end",
                    text=entry_list[0],
                    values=[entry_list[1]],
                    open=True,
                )
        else:
            # add entry as a row:
            # assign "Top Level" as label,
            # "name" as folder name, and
            # a unique row id
            self.tree_dir.insert(
                parent="",
                index="end",
                text="----------------",
                values=[data],
                open=True,
            )

    def get_all_rows(self) -> list[str]:
        row_data = []
        for parent in self.tree_dir.get_children():
            parent_dir = self.tree_dir.item(parent)["values"]
            row_data.append(parent_dir[0])
            for child in self.tree_dir.get_children(parent):
                child_dir = self.tree_dir.item(child)["values"]
                path = f"{parent_dir[0]}/{child_dir.pop()}"
                row_data.append(path)
        return row_data

    def set_data_into_treeview(self, data: list[str]):
        if isinstance(data, list):
            for item in data:
                self._insert_row(item)
        else:
            self._insert_row(data)

    def _rm_custom_dir(self):
        current_item = self.tree_dir.selection()
        self.tree_dir.delete(current_item)

    def __find_row_id_by_name(self, name: str):
        for parent in self.tree_dir.get_children():
            if name in str(self.tree_dir.item(parent)["values"]):
                return parent
            for child in self.tree_dir.get_children(parent):
                if name in self.tree_dir.item(str(child))["values"]:
                    return child
