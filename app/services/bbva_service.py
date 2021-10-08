from app.models.bbva import BBVAModel
from logger import logger


class BBVAService:
    def __init__(self, document):
        self.model = BBVAModel(document)

    def save_statments(self):
        try:
            if not self.model.save_statments():
                return False
            return True
        except Exception as e:
            logger.error(e)
            return False
