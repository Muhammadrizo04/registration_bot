from modeltranslation.translator import TranslationOptions, register

from .models import District, Region, Quarter


# @register(Region)
# class RegionTranslationOptions(TranslationOptions):
#     fields = ("name","name_ru",)


# @register(District)
# class DistrictTranslationOptions(TranslationOptions):
#     fields = ("name",)


# @register(Quarter)
# class QuarterTranslationOptions(TranslationOptions):
#     fields = ('name', )
