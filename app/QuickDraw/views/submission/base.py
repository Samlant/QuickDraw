from typing import Protocol
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.ttk import Notebook, Style, Treeview

from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD

from QuickDraw.views.submission.helper import BaseVars

# from view.styling import BlueRose, create_style
# from view.reg_treeview import RegTreeView


class Presenter(Protocol):
    """This enables us to call funtions from the Presenter
    class, either to send/retrieve data.
    """

    def btn_send_envelopes(self, autosend: bool) -> None:
        ...

    def btn_clear_attachments(self) -> None:
        ...

    def btn_reset_template(self) -> None:
        ...

    def btn_view_template(self) -> None:
        ...

    def btn_save_template(self) -> None:
        ...

    def btn_save_email_settings(self) -> None:
        ...

    def btn_save_folder_settings(self) -> None:
        ...

    def add_qf_registration(self) -> None:
        ...

    def btn_save_registration_settings(self) -> None:
        ...

    def btn_revert_email_settings(self, event) -> None:
        ...

    def btn_revert_folder_settings(self, event) -> None:
        ...

    def btn_revert_registration_settings(self, event) -> None:
        ...

    def set_dropdown_options(self) -> list:
        ...

    def process_quoteform_path(self, drag_n_drop_event) -> None:
        ...

    def process_attachments_path(self, drag_n_drop_event) -> None:
        ...

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        ...

    def _save_signature_image_path(self, path: str) -> None:
        ...

    def save_extra_notes(self, notes: str) -> None:
        ...

    def on_change_template(self, *args, **kwargs) -> None:
        ...

    def on_focus_out(self, field_name: str, current_text: str) -> bool:
        ...


# BR = BlueRose()


class RegColumn(Protocol):
    name: str
    width: int


class Quoteform(Protocol):
    """Stores the characteristics of a specific PDF quoteform.

    Attributes:
        id : standardized name used to ID mapping in config.ini file
        name : user-chosen name for the specific mapping
        all other attrs : required fields from PDF

    """

    id: str
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str

    def values(self) -> tuple[str]:
        ...


class Submission:
    def __init__(
        self,
        positive_value,
        negative_value,
        icon_src: str,
        style: Style,
    ) -> None:
        self._yes = positive_value
        self._no = negative_value
        self.icon = icon_src
        self.style = style
        self.root = TkinterDnD.Tk()

    def assign_private_string_bool_vars(self) -> None:
        """Assigns tkinter-specific attributes so that the getters /
        setters work and other modules do not need to need tkinter.
        """
        vars = BaseVars()
        for var in vars:
            attr_name = f"_{var.__name__.lower()}"
            setattr(self, attr_name, var)

    # main_tab: getters/setters
    @property
    def extra_notes(self) -> str:
        return self._extra_notes_text.get("1.0", "end-1c")

    @extra_notes.deleter
    def extra_notes(self):
        self._extra_notes_text.delete("1.0")

    @property
    def userinput_CC1(self) -> str:
        return self._userinput_CC1.get("1.0", "end-1c")

    @property
    def userinput_CC2(self) -> str:
        return self._userinput_CC2.get("1.0", "end-1c")

    @property
    def use_default_cc_addresses(self) -> bool:
        return self._use_CC_defaults.get()

    @use_default_cc_addresses.setter
    def use_default_cc_addresses(self, usage: bool) -> None:
        self._use_CC_defaults.set(usage)

    @property
    def sw(self) -> str:
        return self._seawave.get()

    @property
    def pt(self) -> str:
        return self._primetime.get()

    @property
    def nh(self) -> str:
        return self._newhampshire.get()

    @property
    def am(self) -> str:
        return self._americanmodern.get()

    @property
    def km(self) -> str:
        return self._kemah.get()

    @property
    def cp(self) -> str:
        return self._concept.get()

    @property
    def yi(self) -> str:
        return self._yachtinsure.get()

    @property
    def ce(self) -> str:
        return self._century.get()

    @property
    def In(self) -> str:
        return self._intact.get()

    @property
    def tv(self) -> str:
        return self._travelers.get()

    @property
    def quoteform(self):
        return self.quoteform_path_box.get("1.0", "end-1c")

    @quoteform.setter
    def quoteform(self, new_attachment: str):
        self.quoteform_path_box.insert("1.0", new_attachment)

    @quoteform.deleter
    def quoteform(self):
        self.quoteform_path_box.delete("1.0", END)

    @property
    def extra_attachments(self):
        return self.extra_attachments_path_box.get("1.0", "end-1c")

    @extra_attachments.setter
    def extra_attachments(self, new_attachment: str):
        self.extra_attachments_path_box.insert("1.0", new_attachment + "\n")

    @extra_attachments.deleter
    def extra_attachments(self):
        self.extra_attachments_path_box.delete("1.0", END)

    # customize_tab: getters/setters
    @property
    def selected_template(self) -> str:
        return self._dropdown_menu_var.get()

    @property
    def address(self) -> str:
        return self._address.get()

    @address.setter
    def address(self, new_address: str) -> None:
        self._address.set(new_address)

    @address.deleter
    def address(self) -> None:
        self._address.set("")

    @property
    def greeting(self) -> str:
        return self._greeting.get()

    @greeting.setter
    def greeting(self, new_greeting: str) -> None:
        self._greeting.set(new_greeting)

    @greeting.deleter
    def greeting(self) -> None:
        self._greeting.set("")

    @property
    def body(self) -> str:
        return self._body_text.get("1.0", "end-1c")

    @body.setter
    def body(self, new_body: str) -> None:
        self._body_text.insert("1.0", new_body)

    @body.deleter
    def body(self) -> None:
        self._body_text.delete("1.0", "end-1c")

    @property
    def outro(self) -> str:
        return self._outro.get()

    @outro.setter
    def outro(self, new_outro: str) -> None:
        self._outro.set(new_outro)

    @outro.deleter
    def outro(self) -> None:
        self._outro.set("")

    @property
    def salutation(self) -> str:
        return self._salutation.get()

    @salutation.setter
    def salutation(self, new_salutation: str) -> None:
        self._salutation.set(new_salutation)

    @salutation.deleter
    def salutation(self) -> None:
        self._salutation.set("")

    # Email settings_tab: getters/setters
    @property
    def default_cc1(self) -> str:
        return self._default_cc1.get()

    @default_cc1.setter
    def default_cc1(self, new_default_cc: str) -> None:
        self._default_cc1.set(new_default_cc)

    @default_cc1.deleter
    def default_cc1(self) -> None:
        self._default_cc1.set("")

    @property
    def default_cc2(self) -> str:
        return self._default_cc2.get()

    @default_cc2.setter
    def default_cc2(self, new_default_cc: str) -> None:
        self._default_cc2.set(new_default_cc)

    @default_cc2.deleter
    def default_cc2(self) -> None:
        self._default_cc2.set("")

    @property
    def username(self) -> str:
        return self._username.get()

    @username.setter
    def username(self, new_username: str):
        self._username.set(new_username)

    @username.deleter
    def username(self) -> None:
        self._username.set("")

    @property
    def sig_image_file(self) -> str:
        return self.sig_image_path_box.get("1.0", "end-1c")

    @sig_image_file.setter
    def sig_image_file(self, new_image_file: str):
        self.sig_image_path_box.delete("1.0", END)
        self.sig_image_path_box.insert("1.0", new_image_file)

    @sig_image_file.deleter
    def sig_image_file(self):
        self.sig_image_path_box.delete("1.0", END)

    # Folder Settings Tab: getters/setters
    @property
    def watch_dir(self) -> str:
        return self._watch_dir.get()

    @watch_dir.setter
    def watch_dir(self, new_watch_dir: str):
        self._watch_dir.set(new_watch_dir)

    @watch_dir.deleter
    def watch_dir(self):
        self._watch_dir.set("")

    @property
    def new_biz_dir(self) -> str:
        return self._new_biz_dir.get()

    @new_biz_dir.setter
    def new_biz_dir(self, new_new_biz_dir: str):
        self._new_biz_dir.set(new_new_biz_dir)

    @new_biz_dir.deleter
    def new_biz_dir(self):
        self._new_biz_dir.set("")

    @property
    def renewals_dir(self) -> str:
        return self._renewals_dir.get()

    @renewals_dir.setter
    def renewals_dir(self, new_renewals_dir: str):
        self._renewals_dir.set(new_renewals_dir)

    @renewals_dir.deleter
    def renewals_dir(self):
        self._renewals_dir.set("")

    @property
    def custom_parent_dir(self) -> str:
        return self._custom_parent_dir.get()

    @custom_parent_dir.setter
    def custom_parent_dir(self, new_custom_parent_dir: str):
        self._custom_parent_dir.set(new_custom_parent_dir)

    @custom_parent_dir.deleter
    def custom_parent_dir(self):
        self._custom_parent_dir.set("")

    @property
    def custom_sub_dir(self) -> str:
        return self._custom_sub_dir.get()

    @custom_sub_dir.setter
    def custom_sub_dir(self, new__custom_sub_dir: str):
        self._custom_sub_dir.set(new__custom_sub_dir)

    @custom_sub_dir.deleter
    def custom_sub_dir(self):
        self._custom_sub_dir.set("")

    # Quoteform Registrations Tab: getters/setters
    @property
    def form_name(self) -> str:
        return self._form_name.get()

    @form_name.deleter
    def form_name(self):
        self._form_name.set("")

    @property
    def fname(self) -> str:
        return self._fname.get()

    @fname.deleter
    def fname(self):
        self._fname.set("")

    @property
    def lname(self) -> str:
        return self._lname.get()

    @lname.deleter
    def lname(self):
        self._lname.set("")

    @property
    def year(self) -> str:
        return self._year.get()

    @year.deleter
    def year(self):
        self._year.set("")

    @property
    def vessel(self) -> str:
        return self._vessel.get()

    @vessel.deleter
    def vessel(self):
        self._vessel.set("")

    @property
    def referral(self) -> str:
        return self._referral.get()

    @referral.deleter
    def referral(self):
        self._referral.set("")

    # @property
    # def quoteform_name(self) -> str:
    #     return self._quoteform_name.get()

    # @quoteform_name.deleter
    # def quoteform_name(self):
    #     self._quoteform_name.set("")

    ### END of Getters/Setters ###

    # Commented out below because it was moved to interface.py

    # def create_UI_obj(self, presenter: Presenter):
    #     """This creates the GUI root,  along with the main
    #     functions to create the widgets.
    #     """
    #     self.root = TkinterDnD.Tk()
    #     self.assign_private_string_bool_vars()
    #     self.assign_window_traits()
    #     self.create_notebook()
    #     self.create_tabs()
    #     self.create_main_tab_widgets(presenter)
    #     self.create_customize_tab_widgets(presenter)
    #     self.create_email_settings_tab_widgets(presenter)
    #     self.create_folder_settings_tab_widgets(presenter)
    #     self.create_quoteform_registrations_tab_widgets(presenter)

    def assign_window_traits(self):
        self.root.geometry("760x600")
        # self.root.configure(background="red")
        self.root.attributes("-topmost", True)
        self.root.title("QuickDraw")
        self.root.attributes("-alpha", 0.95)
        self.root.iconbitmap(self.icon)

    def create_notebook(self):
        self.root.tabControl = Notebook(master=self.root)
        self.root.tabControl.pack(fill="both", pady=0, expand=True)

    def create_tabs(self):
        self.tabs.home = ttk.Frame(self.root.tabControl)
        self.tabs.templates = ttk.Frame(self.root.tabControl)
        self.tabs.email = ttk.Frame(self.root.tabControl)
        self.tabs.dirs = ttk.Frame(self.root.tabControl)
        self.tabs.quoteforms = ttk.Frame(self.root.tabControl)
        self.root.tabControl.add(self.tabs.home, text="Home - Outbox")
        self.root.tabControl.add(self.tabs.templates, text="Email Templates")
        self.root.tabControl.add(self.tabs.email, text="Email Settings")
        self.root.tabControl.add(self.tabs.dirs, text="Folder Settings")
        self.root.tabControl.add(self.tabs.quoteforms, text="Quoteform Registrations")

    def _browse_qf_path(self):
        try:
            dir_name = filedialog.askopenfilename()
            if not dir_name == "":
                self.quoteform_path_box = self.quoteform
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_extra_file_path(self):
        try:
            dir_name = filedialog.askopenfilename()
            if not dir_name == "":
                self.extra_attachments_path_box = self.extra_attachments
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def get_active_focus(self) -> dict:
        return self.root.focus_get()

    def _browse_name_img(self):
        try:
            file_name = filedialog.askopenfile().name
            self.sig_image_path_box.delete("1.0", "end")
            self.sig_image_path_box.insert("1.0", file_name)
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")
        # del self.sig_image_file

    def _upload_img_btn(self):
        try:
            file_path = self.sig_image_path_box.get("1.0", END)
            file_name = ""
            # send URL request to upload img to hosting site
            # insert received response url into text box
            self.sig_image_path_box.delete("1.0", END)
            self.sig_image_path_box.insert("1.0", file_name)
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

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

    def set_start_tab(self, specific_tab: str) -> None:
        if specific_tab == "template":
            self.root.tabControl.select(1)
        elif specific_tab == "email":
            self.root.tabControl.select(2)
        elif specific_tab == "folder":
            self.root.tabControl.select(3)
