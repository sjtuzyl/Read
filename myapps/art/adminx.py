import xadmin
from xadmin import views
from art.models import Tag,Articl

class BaseSetting(object):
    # 主题修改
    enable_themes = False
    use_bootswatch = True

class GlobalSettings(object):
    # 整体配置
    site_title = '美文后台管理系统'
    site_footer = '千锋教育python项目'
    menu_style = 'accordion'  # 菜单折叠
    # 搜索模型
    global_search_models = [Tag, Articl]

    # 模型的图标(参考bootstrap图标插件)
    global_models_icon = {
        Articl: "glyphicon glyphicon-book",
        Tag: "fa fa-cloud"
    }  # 设置models的全局图标
    #设置a
    apps_label_title = {
        'articl':'文章管理'
    }
    apps_icons = {
        'articl':'glyphicon glyphicon-book'
    }


class TagAdmin(object):
    list_display = ['name','add_time']
    search_fields = ['name']

class ArticlAdmin(object):
    list_display = ['title','author','summary','publish_date']
    search_fields = ['title','author']
    style_fields = {'content': 'ueditor'}

xadmin.site.register(views.BaseAdminView,BaseSetting)  #基本后台设置
xadmin.site.register(views.CommAdminView,GlobalSettings)  #通用设置

xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(Articl,ArticlAdmin)