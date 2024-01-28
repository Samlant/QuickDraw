from QuickDraw.helper import open_config


class TemplatesModel:
    def __init__(self) -> None:
        # NAMES replaces get_dropdown_options()
        # TODO Ensure Presenter uses this correctly! Thinka lso about how to institute a carrier class!
        self.names = [
            "Seawave",
            "Prime Time",
            "New Hampshire",
            "American Modern",
            "Kemah Marine",
            "Concept Special Risks",
            "Yachtinsure",
            "Century",
            "Intact",
            "Travelers",
            "Combination: Seawave + Prime Time + New Hampshire",
            "Combination: Prime Time + New Hampshire",
            "Combination: Seawave + New Hampshire",
            "Combination: Seawave + Prime Time",
        ]

    def get_templates(self) -> list[str]:
        """This will replace self.names via automation."""
        config = open_config()
        sections = config.sections()
        template_names = []
        for section in sections:
            if "carrier_" in section:
                template_names.append(section.replace("carrier_", ""))
        return template_names
