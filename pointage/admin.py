from django.contrib import admin
from .models import AtdRecord, Summary, TimeEnter

# Register your models here.
admin.site.register(AtdRecord)
admin.site.register(Summary)
admin.site.register(TimeEnter)