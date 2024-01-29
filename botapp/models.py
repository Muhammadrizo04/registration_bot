from django.db import models
from common.models import BaseModel, Region, District, Quarter


class Direction(BaseModel):
    pass


class BotUsers(BaseModel):
    chat_id = models.BigIntegerField()
    nickname = models.CharField(max_length=120)
    user_lang = models.CharField(max_length=3)
    phone = models.CharField(max_length=15)
    full_name = models.CharField(max_length=80)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="bot_users", null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="bot_users", null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name="bot_users", null=True)
    adress = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.full_name