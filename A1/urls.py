from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Ye line add karni hai
from main_app import views as main_views # Ye line imports mein add karein

urlpatterns = [
    path('admin/', admin.site.urls),
    # Purani logout line ko hata kar ye daalein
    path('accounts/logout/', main_views.custom_logout, name='logout'),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media settings for images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)