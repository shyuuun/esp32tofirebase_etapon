from django.contrib import admin
from .models import SmartBin
# Register your models here.

class smartBinAdmin(admin.ModelAdmin):
    list_display = ("binName", "binDate", "binTime", "battery", "binLevel1", "binLevel2")

admin.site.register(SmartBin, smartBinAdmin)


