import xadmin
from .models import Course


class CourseAdmin(object):
    list_display = ('id', 'time_type', 'name', 'is_on_shelf', 'is_index_recommend', 'is_detail_recommend')
    list_filter = ('time_type', 'name', 'is_on_shelf', 'is_index_recommend', 'is_detail_recommend')
    search_fields = ('id', 'time_type', 'name', 'is_on_shelf', 'is_index_recommend', 'is_detail_recommend')
    model_icon = 'fa fa-book'  # 图标


xadmin.site.register(Course, CourseAdmin)
