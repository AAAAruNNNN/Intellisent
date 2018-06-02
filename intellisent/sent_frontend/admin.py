from django.contrib import admin

# Register your models here.

from .models import Channel, Program, Episode, Tweet

admin.site.register(Channel)
admin.site.register(Program)
admin.site.register(Episode)
admin.site.register(Tweet)