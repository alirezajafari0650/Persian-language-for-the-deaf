from django.contrib import admin

from .models import *

admin.site.register(Word)
admin.site.register(LinkManager)
admin.site.register(WordCategory)
admin.site.register(NewWord)
admin.site.register(Exam)
