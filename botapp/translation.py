from modeltranslation.translator import TranslationOptions, register

from .models import Problem


@register(Problem)
class ProblemTranslationOptions(TranslationOptions):
    fields = ("name",)
