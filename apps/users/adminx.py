import xadmin
from xadmin.layout import Fieldset
from xadmin import views
from .models import User, Banner, Company


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)


# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '西岸小程序后台'
    # 修改footer
    site_footer = '西岸集团'
    # 收起菜单
    menu_style = 'accordion'


# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)


class UserAdmin(object):
    list_display = ('id', 'wx_openid')
    # search_fields = ('wx_openid', 'id', 'nickName', 'gender', 'city', 'country', 'province')
    # list_filter = ('wx_openid', 'id', 'nickName', 'gender', 'city', 'country', 'province')
    model_icon = 'fa fa-user-circle-o'
    show_detail_fileds = ('id', 'wx_openid')
    relfield_style = 'fk-ajax'
    base_list_display = ('id', 'wx_openid')

    model_fields = ('id', 'wx_openid')
    form_layout = (
        Fieldset(None,
                 "avatarUrl", **{"style": "display:None"}
                 ),
        Fieldset(None,
                 "nickName", **{"style": "display:None"}
                 ),
        Fieldset(None,
                 "gender", **{"style": "display:None"}
                 ),
        Fieldset(None,
                 "city", **{"style": "display:None"}
                 ),
        Fieldset(None,
                 "country", **{"style": "display:None"}
                 ),
        Fieldset(None,
                 "province", **{"style": "display:None"}
                 ),
    )


class BannerAdmin(object):
    list_display = ('title', 'id', 'image', 'index', 'is_on_shelf', 'project_id')
    list_filter = ('title', 'id', 'image', 'index', 'is_on_shelf', 'project_id')
    search_fields = ('title', 'id', 'image', 'index', 'is_on_shelf', 'project_id')
    model_icon = 'fa fa-chevron-circle-right'


class CompanyAdmin(object):
    # list_display = ()
    # search_fields = ()
    # list_filter = ()
    model_icon = 'fa fa-asl-interpreting'
    style_fields = {"description": "ueditor"}


# class WxFormAdmin(object):
#     list_display = ('wx_openid', 'form_id', 'source', 't_created')
#     search_fields = ('wx_openid', 'form_id', 'source',)
#     list_filter = ('wx_openid', 'source', 't_created')
#     model_icon = 'fa fa-wpforms'


xadmin.site.register(User, UserAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Company, CompanyAdmin)
