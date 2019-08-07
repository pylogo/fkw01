from rest_framework.serializers import ModelSerializer
from apps.shop import models


class CardSerializers(ModelSerializer):
    class Meta:
        # 卡密 所属商品 售出状态
        model = models.Card
        fields = ['id', 'commodity_info', 'card_type']
