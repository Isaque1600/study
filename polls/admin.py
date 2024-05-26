from django.contrib import admin

from .models import Questions, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInLine]


admin.site.register(Questions, QuestionsAdmin)

# Register your models here.
