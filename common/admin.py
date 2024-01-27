from django.contrib import admin

from .models import Region, District, Quarter


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


class QuarterInline(admin.TabularInline):
    model = Quarter
    extra = 1


class RegionAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]
    list_display = ('name', )
    search_fields = ('name', )


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region', )
    search_fields = ('name', )
    inlines = [QuarterInline]


class QuarterAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    list_filter = ('district', )
    search_fields = ('name', )


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Quarter, QuarterAdmin)
