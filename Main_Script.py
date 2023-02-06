from model import Model
from view import TkView
from presenter import Presenter

def main() -> None:
    model = Model()
    view = TkView()
    presenter = Presenter(model, view)
    presenter.start_program()

main()