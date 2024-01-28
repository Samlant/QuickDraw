from QuickDraw.views.submission.helper import ALL_TABS
from QuickDraw.views.submission.base.window import Window


class ViewInterface(Window):
    def __init__(self):
        super().__init__()

    # main_tab: getters/setters
    @property
    def home_values(self) -> dict[str, str]:
        return {
            "quoteform": self.quoteform,
            "extra_attachments": self.extra_attachments,
            "extra_notes": self.extra_notes,
            "userinput_CC1": self.userinput_CC1,
            "userinput_CC2": self.userinput_CC2,
            "use_CC_defaults": self.use_CC_defaults,
        }

    @home_values.setter
    def home_values(self, save_data: dict[str, str | bool]) -> None:
        for attr_name, value in save_data.items():
            setattr(self, attr_name, value)

    @home_values.deleter
    def home_values(self):
        for attr in ALL_TABS["home"].keys():
            delattr(self, attr)

    @property
    def template_values(self) -> dict[str, str]:
        return {
            "selected_template": self.selected_template,
            "address": self.address,
            "greeting": self.greeting,
            "body": self.body,
            "outro": self.outro,
            "salutation": self.salutation,
        }

    @template_values.setter
    def template_values(self, save_data: dict[str, str | bool]) -> None:
        for attr_name, value in save_data.items():
            setattr(self, attr_name, value)

    @template_values.deleter
    def template_values(self):
        for attr in ALL_TABS["templates"].keys():
            delattr(self, attr)

    @property
    def email_values(self) -> dict[str, str]:
        return {
            "default_cc1": self.default_cc1,
            "default_cc2": self.default_cc2,
            "username": self.username,
            "sig_image_file_path": self.sig_image_file_path,
        }

    @email_values.setter
    def email_values(self, save_data: dict[str, str | bool]) -> None:
        for attr_name, value in save_data.items():
            setattr(self, attr_name, value)

    @email_values.deleter
    def email_values(self):
        for attr in ALL_TABS["email"].keys():
            delattr(self, attr)

    @property
    def dirs_values(self) -> dict[str, str]:
        return {
            "watch_dir": self.watch_dir,
            "new_biz_dir": self.new_biz_dir,
            "renewals_dir": self.renewals_dir,
            "custom_parent_dir": self.custom_parent_dir,
            "custom_sub_dir": self.custom_sub_dir,
        }

    @dirs_values.setter
    def dirs_values(self, save_data: dict[str, str | bool]) -> None:
        for attr_name, value in save_data.items():
            setattr(self, attr_name, value)

    @dirs_values.deleter
    def dirs_values(self):
        for attr in ALL_TABS["dirs"].keys():
            delattr(self, attr)

    @property
    def quoteforms_values(self) -> dict[str, str]:
        return {
            "form_name": self.form_name,
            "fname": self.fname,
            "lname": self.lname,
            "year": self.year,
            "vessel": self.vessel,
            "referral": self.referral,
        }

    @quoteforms_values.setter
    def quoteforms_values(self, save_data: dict[str, str | bool]) -> None:
        for attr_name, value in save_data.items():
            setattr(self, attr_name, value)

    @quoteforms_values.deleter
    def quoteforms_values(self):
        for attr in ALL_TABS["quoteforms"].keys():
            delattr(self, attr)

    @property
    def extra_notes(self) -> str:
        return self._extra_notes.get("1.0", "end-1c")

    @extra_notes.deleter
    def extra_notes(self):
        self._extra_notes.delete("1.0")

    @property
    def userinput_CC1(self) -> str:
        return self._userinput_CC1.get("1.0", "end-1c")

    @property
    def userinput_CC2(self) -> str:
        return self._userinput_CC2.get("1.0", "end-1c")

    @property
    def use_CC_defaults(self) -> bool:
        return self._use_CC_defaults.get()

    @use_CC_defaults.setter
    def use_CC_defaults(self, usage: bool) -> None:
        self._use_CC_defaults.set(usage)

    @property
    def seawave(self) -> str:
        return self._seawave.get()

    @property
    def primetime(self) -> str:
        return self._primetime.get()

    @property
    def newhampshire(self) -> str:
        return self._newhampshire.get()

    @property
    def americanmodern(self) -> str:
        return self._americanmodern.get()

    @property
    def kemah(self) -> str:
        return self._kemah.get()

    @property
    def concept(self) -> str:
        return self._concept.get()

    @property
    def yachtinsure(self) -> str:
        return self._yachtinsure.get()

    @property
    def century(self) -> str:
        return self._century.get()

    @property
    def intact(self) -> str:
        return self._intact.get()

    @property
    def travelers(self) -> str:
        return self._travelers.get()

    @property
    def quoteform(self):
        return self._quoteform.get("1.0", "end-1c")

    @quoteform.setter
    def quoteform(self, new_attachment: str):
        self._quoteform.insert("1.0", new_attachment)

    @quoteform.deleter
    def quoteform(self):
        self._quoteform.delete("1.0", "end")

    @property
    def extra_attachments(self):
        return self._extra_attachments.get("1.0", "end-1c")

    @extra_attachments.setter
    def extra_attachments(self, new_attachment: str):
        self._extra_attachments.insert("1.0", new_attachment + "\n")

    @extra_attachments.deleter
    def extra_attachments(self):
        self._extra_attachments.delete("1.0", "end")

    # customize_tab: getters/setters
    @property
    def selected_template(self) -> str:
        return self._selected_template.get()

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
        return self._body.get("1.0", "end-1c")

    @body.setter
    def body(self, new_body: str) -> None:
        self._body.insert("1.0", new_body)

    @body.deleter
    def body(self) -> None:
        self._body.delete("1.0", "end-1c")

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
    def sig_image_file_path(self) -> str:
        return self._sig_image_file_path.get("1.0", "end-1c")

    @sig_image_file_path.setter
    def sig_image_file_path(self, new_image_file: str):
        self._sig_image_file_path.delete("1.0", "end")
        self._sig_image_file_path.insert("1.0", new_image_file)

    @sig_image_file_path.deleter
    def sig_image_file_path(self):
        self._sig_image_file_path.delete("1.0", "end")

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