import uuid

from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel, Region, District, Quarter


class Interest(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Interest Name"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "interests"
        """Index for iexact lookups"""
        indexes = [
            models.Index(
                Upper("name_uz").desc(), name="interest_name_uz_upper_index"
            ),
            models.Index(
                Upper("name_ru").desc(), name="interest_name_ru_upper_index"
            ),
        ]


class Education(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Education Name"))
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='education', verbose_name=_("Interest"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "education"
        """Index for iexact lookup"""
        indexes = [
            models.Index(
                Upper("name_uz").desc(), name="education_name_uz_upper_index"
            ),
            models.Index(
                Upper("name_ru").desc(), name="education_name_ru_upper_index"
            ),
        ]


class Course(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_("Course Name"))
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='course', verbose_name=_("Education"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "course"
        """Index for iexact lookup"""
        indexes = [
            models.Index(
                Upper("name_uz").desc(), name="course_name_uz_upper_index"
            ),
            models.Index(
                Upper("name_ru").desc(), name="course_name_ru_upper_index"
            ),
        ]



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

    def __str__(self) -> str:
        return self.full_name
    

