from app.models.hsbc import HSBCModel


class HSBCService:
    def __init__(self, document):
        self.model = HSBCModel(document)

    def save_statments(
        self,
        bank,
    ):
        return self.model.save_statments(bank, "", "")
