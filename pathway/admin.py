from django.contrib import admin

from .models import Industry, Firm, DisplayStage


class SectionInLine(admin.StackedInline):
    model = DisplayStage


class FirmAdmin(admin.ModelAdmin):
    inlines = [
        SectionInLine
    ]


admin.site.register(Industry)
admin.site.register(Firm, FirmAdmin)
