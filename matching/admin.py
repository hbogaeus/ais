from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Question, Category, Survey, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns

class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('category',)

class CategoryInline(admin.TabularInline):
    model = Category

class SurveyAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, QuestionInline]

class AnswerInline(admin.StackedInline):
    fields = ('question', 'ans')
    readonly_fields = ('question',)

class TextAnsInline(AnswerInline):
    model = TextAns

class ChoiceAnsInline(AnswerInline):
    model = ChoiceAns

class IntegerAnsInline(AnswerInline):
    model = IntegerAns

class BooleanAnsInline(AnswerInline):
    model = BooleanAns

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('exhibitor',)
    inlines = [TextAnsInline, ChoiceAnsInline, IntegerAnsInline, BooleanAnsInline]
    readonly_fields = ('survey', 'exhibitor')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
#admin.site.register(ChoiceAns)
#admin.site.register(TextAns)
#admin.site.register(BooleanAns)
#admin.site.register(Question)
