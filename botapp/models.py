import uuid

from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel, Region, District, Quarter


class Interest(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Interest Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Interest Name RU"))

    def __str__(self) -> str:
        return self.name



class Education(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Education Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Education Name RU"))
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='education', verbose_name=_("Interest"))

   
class Course(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Course Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Course Name RU"))
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='course', verbose_name=_("Education"))

    



class BotUser(BaseModel):
    chat_id = models.BigIntegerField()
    full_name = models.CharField(max_length=80, blank=True)
    nick_name = models.CharField(max_length=120)
    user_lang = models.CharField(max_length=3, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    age = models.CharField(max_length=20, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    adress = models.CharField(max_length=60)
    user_state = models.CharField(max_length=50)
    selected_district_id = models.CharField(max_length = 10)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    problems = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.full_name
    

