from modeltranslation.translator import register, TranslationOptions

from apps.order import models


@register(models.Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)
