from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Spec)
class SpecTranslationOptions(TranslationOptions):
    fields = ('key', 'value')

