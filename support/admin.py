from django.contrib import admin

# Register your models here.
from .models import Ticket,Report
admin.site.register(Ticket)
admin.site.register(Report)
