from django.contrib import admin
from .models import SchoolFee,Student,Ticket

# Register your models here.

admin.site.register(SchoolFee)
admin.site.register(Student)
admin.site.register(Ticket)