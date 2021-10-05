from app.models.banorte import BanorteModel
from logger import logger


class BanorteService:
    def __init__(self, document):
        self.model = BanorteModel(document)

    def save_statments(self):
        try:
            if not self.model.save_statments():
                return False
            return True
        except Exception as e:
            logger.error(e)
            return False

