from django.contrib import admin

# Register your models here.
from .models import Sala,Peticio,Concesio

admin.site.register(Sala)
#admin.site.register(Peticio)

# Define the admin class
class PeticioAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Peticio, PeticioAdmin)

# Define the admin class
class ConcesioAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Concesio, ConcesioAdmin)
