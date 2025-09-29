from django.contrib import admin
from .models import *

# Register your models here.
# admin pass=0001
admin.site.register(User)

admin.site.register(Appointment)
admin.site.register(MedicalRecord)