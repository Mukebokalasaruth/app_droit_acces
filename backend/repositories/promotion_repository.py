from models.promotion import Promotion


class PromotionRepository:

    # LISTE PROMOTIONS
    @staticmethod
    def get_all():

        return Promotion.query.all()