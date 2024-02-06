from django.contrib import admin

from .models import Region, District, Quarter

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region

class DistrictResource(resources.ModelResource):
    class Meta:
        model = District

class QuarterResource(resources.ModelResource):
    class Meta:
        model = Quarter

class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


class QuarterInline(admin.TabularInline):
    model = Quarter
    extra = 1


class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource
    inlines = [DistrictInline]
    list_display = ('name_uz', 'name_ru')
    search_fields = ('name_uz', 'name_ru')


class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource
    list_display = ('name_uz', 'name_ru', 'region')
    list_filter = ('region', )
    search_fields = ('name_uz', 'name_ru' )
    inlines = [QuarterInline]


class QuarterAdmin(ImportExportModelAdmin):
    resource_class = QuarterResource
    list_display = ('name_uz', 'name_ru', 'district')
    list_filter = ('district', )
    search_fields = ('name_uz', 'name_ru')


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Quarter, QuarterAdmin)
