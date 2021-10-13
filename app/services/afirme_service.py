from app.models.afirme import AfirmeModel
from logger import logger


class AfirmeService:
    def __init__(self, document):
        self.model = AfirmeModel(document)

    def save_statments(self):
        try:
            self.model.save_statments()
        except Exception as e:
            logger.error(e)
            return None
