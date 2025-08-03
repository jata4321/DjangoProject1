from django.contrib import admin
from .models import Country, Type, Tenor

# Register your models here.
admin.site.register(Country, admin.ModelAdmin)
admin.site.register(Type, admin.ModelAdmin)
admin.site.register(Tenor, admin.ModelAdmin)
