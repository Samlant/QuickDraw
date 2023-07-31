from pathlib import Path

from model.config import ConfigWorker

path = Path("app") / "resources" / "configurations.ini"
# path = str(Path.joinpath(path) / "resources" / "configurations.ini")
print(path.resolve())

work = ConfigWorker(path)

# save = work.get_value({"section_name": "General settings", "key": "client_id"})
# print(save)

section = work.get_section(section_name="graph_api")
client_id = section.get("client_id").value
print(client_id)

# work.add_section("graph_api")
