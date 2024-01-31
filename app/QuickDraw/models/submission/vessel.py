from dataclasses import dataclass


@dataclass(frozen=True)
class Vessel:
    year: str
    make: str

    def __str__(self):
        return f"{self.year} {self.make}"
