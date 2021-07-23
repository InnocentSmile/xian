import xadmin
from .models import Activity, Signupsheet


class ActivityAdmin(object):
    list_display = ("id","name","into_img","master_img","is_on_shelf")
    list_filter = ("name", "is_on_shelf")
    search_fields = ("name",)
    model_icon = 'fa fa-free-code-camp'  # 图标


class SignupsheetAdmin(object):
    list_display = ("user_id","name","contact_info","email", "activity_id")
    list_filter = ("user_id", "activity_id","name","contact_info","email")
    search_fields = ("user_id","activity_id""name","contact_info","email")


xadmin.site.register(Activity, ActivityAdmin)
xadmin.site.register(Signupsheet, SignupsheetAdmin)
