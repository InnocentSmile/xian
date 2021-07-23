import xadmin
from .models import UserFavorite, Resource, RDUser, Appointment


class UserFavoriteAdmin(object):
    list_display = ('user_id', 'fav_id', 'fav_type')
    search_fields = ('user_id', 'fav_id', 'fav_type')
    list_filter = ('user_id', 'fav_id', 'fav_type')
    model_icon = 'fa fa-hand-scissors-o'


class ResourceAdmin(object):
    list_display = ('name', "index", "is_on_shelf")
    search_fields = ('name', "index", "is_on_shelf")
    list_filter = ('name', "index", "is_on_shelf")
    model_icon = 'fa fa-file'


class RDUserAdmin(object):
    list_display = ('user_id', 'name', 'id', 'contact_info', 'email', 'is_subscribe')
    search_fields = ('user_id', 'name', 'id', 'contact_info', 'email', 'is_subscribe')
    list_filter = ('user_id', 'name', 'id', 'contact_info', 'email', 'is_subscribe')
    model_icon = 'fa fa-wpforms'


class AppointmentAdmin(object):
    list_display = ('id', 'user_id', 'name', 'contact_info', 'email', 'city', 'msg', 'is_subscribe')
    search_fields = ('user_id', 'name', 'contact_info', 'email', 'city', 'msg', 'is_subscribe')
    list_filter = ('user_id', 'name', 'contact_info', 'email', 'city', 'msg', 'is_subscribe')
    model_icon = 'fa fa-life-ring'


xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(Resource, ResourceAdmin)
xadmin.site.register(RDUser, RDUserAdmin)
xadmin.site.register(Appointment, AppointmentAdmin)
