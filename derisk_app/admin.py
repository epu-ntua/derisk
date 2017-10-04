from django.contrib import admin
from derisk_app.models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    pass


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    pass


@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    pass
