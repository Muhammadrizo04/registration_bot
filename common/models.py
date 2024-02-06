import uuid

from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Region Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Region Name RU"))

    def __str__(self) -> str:
        return self.name_uz

    # class Meta:
    #     db_table = "regions"
    #     """Index for iexact lookups"""
    #     indexes = [
    #         models.Index(
    #             Upper("name_uz").desc(), name="region_name_uz_upper_index"
    #         ),
    #         models.Index(
    #             Upper("name_ru").desc(), name="region_name_ru_upper_index"
    #         ),
    #     ]


class District(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("District Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("District Name RU"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name=_("Region"))

    def __str__(self) -> str:
        return self.name_ru

    # class Meta:
    #     db_table = "districts"
    #     """Index for iexact lookup"""
    #     indexes = [
    #         models.Index(
    #             Upper("name_uz").desc(), name="district_name_uz_upper_index"
    #         ),
    #         models.Index(
    #             Upper("name_ru").desc(), name="district_name_ru_upper_index"
    #         ),
    #     ]


class Quarter(BaseModel):
    name_uz = models.CharField(max_length=250, verbose_name=_("Quarter Name"))
    name_ru = models.CharField(max_length=250, verbose_name=_("Quarter Name RU"))
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='quarters', verbose_name=_("District"))

    def __str__(self) -> str:
        return self.name_uz

    # class Meta:
    #     db_table = "quarters"
    #     """Index for iexact lookup"""
    #     indexes = [
    #         models.Index(
    #             Upper("name_uz").desc(), name="quarter_name_uz_upper_index"
    #         ),
    #         models.Index(
    #             Upper("name_ru").desc(), name="quarter_name_ru_upper_index"
    #         ),
    #     ]
