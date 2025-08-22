from django.contrib import admin
from .models import TestCategory, TestPrompt, FourOptionQuestion, YesNoQuestion, UserFourOptionAnswer, UserYesNoAnswer

# Register your models here.

admin.site.register(TestCategory)
admin.site.register(TestPrompt)
admin.site.register(FourOptionQuestion)
admin.site.register(YesNoQuestion)
