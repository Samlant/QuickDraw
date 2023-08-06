from pathlib import Path
import time
from typing import Protocol


class Presenter(Protocol):
    def trigger_new_file(self):
        ...


class DirWatch:
    "Watches a specific directory for any new files and sends a notification when triggered."

    def __init__(self, path_to_watch: str) -> None:
        self.path = path_to_watch
        self.presenter = None

    def assign_presenter(self, presenter: Presenter) -> None:
        self.presenter = presenter

    def begin_watch(self) -> None:
        before = dict([(f, None) for f in Path.iterdir(self.path)])
        while 1:
            time.sleep(2)
            after = dict([(f, None) for f in Path.iterdir(self.path)])
            added = [f for f in after if not f in before]
            if added:
                new_file = Path(added[0])
                if new_file.suffix == ".pdf":
                    print("New file detected.")
                    print("triggering presenter's new file function.")
                    file_path = Path.joinpath(self.path) / new_file.name
                    self.presenter.trigger_new_file(file=file_path)
            before = dict([(f, None) for f in Path.iterdir(self.path)])
