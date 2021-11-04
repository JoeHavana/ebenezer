from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required

from core.newsletter import views as newsletter_views
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from .api import api_router # Cap-34

#from search import views as search_views

urlpatterns = [

    path('cpanel/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('comments/', include('django_comments_xtd.urls')),

    path('api/', api_router.urls),  # Cap-34
    path('sitemap.xml', sitemap),
    path('accounts/', include('allauth.urls')),  # Delete 'accounts/'

# REST-Framework
	# USERS:
    #path('apis/account/', include('core.users.api.urls', 'account_api')),
    path('apis/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('apis/refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),

# Vanilla Django
    path('article/<slug>/', ItemDetail, name="product-detail"),
    path('search-by/', SearchProducts.as_view(), name="search-products"), # Revisar

    path('category/', AllCategories.as_view(), name="all-categories"), # Revisar
    path('categories/', AllCategories.as_view(), name="all-categories"), # Revisar
    path('category/<slug>/', categoryDetail, name="category-detail"), # Revisar

# Newsletter App 
    path('newsletter-subscribe/', newsletter_views.newsletter_signup, name="newsletter_signup"),
    path('newsletter-unsubscribe/', newsletter_views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    path('newsletter-control/', login_required(newsletter_views.control_newsletter), name="control_newsletter"),
    path('newsletter-list/', login_required(newsletter_views.newsletter_list), name="newsletter_list"),
    path('newsletter/<pk>/', login_required(newsletter_views.newsletter_detail), name="newsletter_detail"),
    path('newsletter/edit/<pk>/', login_required(newsletter_views.newsletter_edit), name="newsletter_edit"),
    path('newsletter/del/<pk>/', login_required(newsletter_views.newsletter_delete), name="newsletter_delete"),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# Django_Debug_Toolbar:
    #import debug_toolbar
    #urlpatterns = [
    #    path('__debug__/', include(debug_toolbar.urls)),
    #] + urlpatterns

# + i18n_patterns (
urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]