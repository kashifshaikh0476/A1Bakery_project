from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from main_app import views as main_views 

# Sitemap imports
from django.contrib.sitemaps.views import sitemap
from main_app.sitemaps import StaticViewSitemap

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin/', main_views.create_admin),
    path('accounts/logout/', main_views.custom_logout, name='logout'),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)