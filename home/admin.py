from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from django.contrib.auth.admin import UserAdmin
from django_comments_xtd.admin import XtdCommentsAdmin
from .models import *
from core.blog.models import *
from core.newsletter.models import *
from core.custompage.models import *
from core.store.models import *
from core.users.models import *

# Next could be declarated at the URLs
admin.site.index_title=f'Administrador de Órdenes'
admin.site.site_header=f'Panel de Control'
admin.site.site_title=f'Administrador'

#######################  Store APP ########################################################

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    #exclude = ('slug', 'updated_at',)


############################################################################
###########################     Wagtail Admin   ############################
############################################################################

class ItemCategoryAdmin(ModelAdmin):

    model = ItemCategory
    menu_label = "Card Categories"
    menu_icon = "pick"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("category_name", "priority", "will_be_recomended",)
    search_fields = ("category_name", "priority", "will_be_recomended",)
    list_filter = ("category_name", "priority", "will_be_recomended",)
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    prepopulated_fields = {'slug' : ('category_name',)}


class ItemAdmin(ModelAdmin):
    """Item admin."""

    model = Item
    menu_label = "Cards"
    menu_icon = "pick"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_export = ("title",)
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    prepopulated_fields = {'slug' : ('title',)}


class StoreGroup(ModelAdminGroup):
    menu_label = "Categorized Cards"
    menu_icon = "pick"
    menu_order = 110
    items = (ItemCategoryAdmin, ItemAdmin,) #AgregosAdmin


modeladmin_register(StoreGroup)
############################ END Store App ###########################################
############################ Newsletter APP - Wagtail Admin  ####################################
class NewsletterUserAdmin(ModelAdmin):
    model = NewsletterUser
    menu_label = "Subscribers"
    menu_icon = "fa-users"
    menu_order = 292
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "email", "email_verified", "date_added",)
    search_fields = ("name", "email", "email_verified", "date_added",)
    list_filter = ("date_added", "email_verified")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    list_export = ("name", "email", "email_verified", "date_added",)
    #prepopulated_fields = {'slug' : ('category_name',)}


class NewsletterAdmin(ModelAdmin):
    model = Newsletter
    menu_label = "Create Newslatter"
    menu_icon = "fa-file"
    menu_order = 293
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("subject", "status",)
    list_filter = ("status",)
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50


class NewsletterGroup(ModelAdminGroup):
    menu_label = "Newsletter"
    menu_icon = "fa-envelope"
    menu_order = 111
    items = (NewsletterUserAdmin, NewsletterAdmin)

modeladmin_register(NewsletterGroup)
############################ END Newsletter APP - Wagtail Admin  ####################################

################################### Users App #################################
@admin.register(User)
class DjangoUserAdmin(admin.ModelAdmin):
    pass

class WagtailUserAdmin(ModelAdmin): # UserAdmin class
    model = User
    menu_label = "Users XTD"
    menu_icon = "fa-user"
    menu_order = 189
    list_per_page = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['username', 'email', 'first_name', 'last_login']
    list_display_links = [ 'email', 'username', 'first_name', 'last_login', 'username','first_name','last_name','city_address','country','gender','ocupation']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'last_login']
    list_filter = ['ocupation', 'gender',]
    empty_value_display = '------'
    list_select_related = True
    list_export = (
        'id',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'last_name',
        "phone",
        "website",
        "street_address",
        "suite_address",
        "city_address",
        "zipcode",
        "country",
        "gender",
        "date_of_birth",
        "ocupation",
    )


modeladmin_register(WagtailUserAdmin)