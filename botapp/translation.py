from modeltranslation.translator import TranslationOptions, register

from .models import *


@register(Interest)
class InterestTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', )
