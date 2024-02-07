import uuid

from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel, Region, District, Quarter


class Interest(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Interest Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Interest Name RU"))

    def __str__(self) -> str:
        return self.name_uz



class Education(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Education Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Education Name RU"))
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='education', verbose_name=_("Interest"))

    def __str__(self) -> str:
        return self.name_uz

class Category(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Category Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Category Name RU"))
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='category', verbose_name=_("Education"))


    def __str__(self) -> str:
        return self.name_uz
    

class Course(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Course Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Course Name RU"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='course', verbose_name=_("Education"))

    def __str__(self) -> str:
        return self.name_uz

class Problem(BaseModel):
    name_uz = models.CharField(max_length=100, verbose_name="Problem Name")
    name_ru = models.CharField(max_length=100, verbose_name="Problem Name RU")

    def __str__(self) -> str:
        return self.name_uz



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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="bot_users", null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name
    

