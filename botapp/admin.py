from .models import *
from django.contrib import admin

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class CourseInline(admin.TabularInline):
    model = Course
    extra = 2

class InterestAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    list_display = ('name_uz', )
    search_fields = ('name_uz', )

class EducationAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'interest')
    list_filter = ('interest', )
    search_fields = ('name_uz', )
    inlines = [CategoryInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'education')
    list_filter = ('education',)
    search_fields = ('name_uz',)
    inlines = [CourseInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'category')
    list_filter = ('category', )
    search_fields = ('name_uz', )


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru')


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'full_name', 'nick_name', 'phone_number', 'region', 'district', 'quarter')
    readonly_fields = ['selected_district_id']

admin.site.register(Interest, InterestAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Problem, ProblemAdmin)
