from Model.model import Model, ConfigWorker
from View.view import TkView
from Presenter.presenter import Presenter


def main() -> None:
    model = Model()
    view = TkView()
    configworker = ConfigWorker()
    presenter = Presenter(model, view, configworker)
    presenter.start_program()


if __name__ == "__main__":
    main()
