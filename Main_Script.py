from model import Model
from view import View
from presenter import Presenter

def main() -> None:
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    presenter.start_program()

main()