from dataclasses import dataclass, field
import itertools

"""
USAGE:

a = Carrier(
    name="FedEx",
    id="1234567890",
    address="123 Main St.",
    greeting="Dear valued customer,\n\n",
    body="We are pleased to inform you that your package has been delivered on ",
    outro="Sincerely,\nThe FedEx Team",
    salutation="Best Regards",
)
b = Carriers(
    name="Combination: UPS and FedEx",
    id="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    address="456 Oak Dr.",
    greeting="Wassup?",
    body="One or both of our packages were delivered on ",
    outro="Peace Out,\nThe UPS & FedEx Teams",
    salutation="Love, Peace & Upside Down",
)
"""


@dataclass
class Carrier:
    _ids = itertools.count(0)
    name: str
    id: str
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str

    def __post_init__(self):
        self.add_one_instance()

    @classmethod
    def num_of_all_instances(cls):
        return cls._ids

    @classmethod
    def add_one_instance(cls):
        next(cls._ids)


@dataclass(kw_only=True)
class Carriers(Carrier):
    num_of_carriers: int = field(init=False)
    names: list[str] = field(init=False)

    def __post_init__(self):
        self.names = self.id_carriers()
        self.num_of_carriers = len(self.names)
        super().__post_init__()

    def id_carriers(self) -> list[str]:
        name = self.name.removeprefix("Combination: ")
        names = name.split(" and ")
        return names
