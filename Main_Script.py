from model import Model
from model_config import ConfigWorker
from view import TkView
from presenter import Presenter


POSITIVE_SUBMISSION_VALUE = "submit"
NEGATIVE_SUBMISSION_VALUE = "pass"


def main() -> None:
    configworker = ConfigWorker()
    model = Model(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    view = TkView(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    presenter = Presenter(model=model, view=view, config_worker=configworker)
    presenter.start_program()


if __name__ == "__main__":
    main()
