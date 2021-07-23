import xadmin
from .models import Country, Project, ProApartment, ProBanner, ProVideo


class CountryAdmin(object):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    model_icon = 'fa fa-cube'


class ProjectAdmin(object):
    list_display = (
        'name', 'city', 'designer', 'start_time', "finish_time", "country", "is_on_shelf",
        "is_index_recommend",
        "is_detail_recommend")
    list_filter = (
        'name', 'city', 'designer', 'start_time', "finish_time", "country", "is_on_shelf",
        "is_index_recommend",
        "is_detail_recommend")
    search_fields = (
        'name', 'city', 'designer', 'start_time', "finish_time", "country", "is_on_shelf",
        "is_index_recommend",
        "is_detail_recommend")
    model_icon = 'fa fa-product-hunt'
    style_fields = {"pro_description": "ueditor"}


class ProApartmentAdmin(object):
    list_display = ("name", "project", "house_area")
    list_filter = ("name", "project", "house_area")
    search_fields = ("name", "project", "house_area")
    model_icon = 'fa fa-pie-chart'


class ProBannerAdmin(object):
    list_display = ("name", "project")
    list_filter = ("name", "project")
    search_fields = ("name", "project")
    model_icon = 'fa fa-chevron-circle-right'


class ProVideoAdmin(object):
    list_display = ("name", "project",)
    list_filter = ("name", "project",)
    search_fields = ("name", "project",)
    model_icon = 'fa fa-file-video-o'


xadmin.site.register(Country, CountryAdmin)
xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(ProApartment, ProApartmentAdmin)
xadmin.site.register(ProBanner, ProBannerAdmin)
xadmin.site.register(ProVideo, ProVideoAdmin)
