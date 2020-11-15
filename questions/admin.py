from django.contrib import admin

from .models import QuestionPack, Question, FirmQuestionPackConnector, Stage


class SectionInLine(admin.StackedInline):
    model = Question

class SectionInLine2(admin.StackedInline):
    model = FirmQuestionPackConnector


class QuestionPackAdmin(admin.ModelAdmin):
    inlines = [
        SectionInLine,
        SectionInLine2
    ]


admin.site.register(QuestionPack, QuestionPackAdmin)
admin.site.register(Stage)