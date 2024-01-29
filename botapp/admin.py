from .models import Direction, BotUser
from django.contrib import admin


class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'full_name', 'nick_name', 'phone_number', 'region', 'district', 'quarter', 'direction')


admin.site.register(Direction, DirectionAdmin)
admin.site.register(BotUser, BotUserAdmin)