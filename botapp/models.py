from django.db import models
from common.models import BaseModel, Region, District, Quarter


class Direction(BaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class BotUser(BaseModel):
    chat_id = models.BigIntegerField()
    full_name = models.CharField(max_length=80)
    nick_name = models.CharField(max_length=120)
    user_lang = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=15)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="bot_users", null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="bot_users", null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name="bot_users", null=True)
    adress = models.CharField(max_length=60)
    direction = models.ForeignKey(
        Direction, on_delete=models.SET_NULL, null=True, related_name="bot_users"
    )

    def __str__(self) -> str:
        return self.full_name