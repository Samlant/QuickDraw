from datetime import datetime
import calendar


class AlertModel:
    def __init__(self) -> None:
        pass

    def get_current_month(self) -> str:
        return calendar.month_name[datetime.today().month]

    def get_next_months(self) -> list[str]:
        current_month = datetime.now().month
        return [
            calendar.month_name[
                (
                    (current_month + i) % 12
                    if current_month + i != 12
                    else (current_month + i)
                )
            ].lower()
            for i in range(0, 3)
        ]
