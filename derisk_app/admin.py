from django.contrib import admin
from derisk_app.models import *
# Register your models here.

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    pass
@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    pass
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass