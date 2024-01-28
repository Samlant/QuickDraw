class AllocateModel:
    def __init__(self):
        pass

    def process_user_choice(
        self,
        all_markets: dict[str, any],
        current_submission,
    ) -> None:
        list_mrkts = []
        for market, value in all_markets.items():
            if value == 1:
                mrkt = market.upper()
                list_mrkts.append(mrkt)
            else:
                pass
        current_submission.status = "SUBMIT TO MRKTS"
        current_submission.markets = list_mrkts
