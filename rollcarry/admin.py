from django.contrib import admin
from .models import Bond

# Register your models here.
admin.site.site_header = "RollCarry Administration"
admin.site.register(Bond)
