from django.contrib import admin

# Register your models here.

from .models import Channel, Program, Episode

admin.site.register(Channel)
admin.site.register(Program)
admin.site.register(Episode)
