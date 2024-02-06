from .models import *
from django.contrib import admin

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class InterestAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    list_display = ('name', )
    search_fields = ('name', )

class EducationAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest')
    list_filter = ('interest', )
    search_fields = ('name', )
    inlines = [CourseInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'education')
    list_filter = ('education', )
    search_fields = ('name', )



class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'full_name', 'nick_name', 'phone_number', 'region', 'district', 'quarter')
    readonly_fields = ['selected_district_id']

admin.site.register(Interest, InterestAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(BotUser, BotUserAdmin)