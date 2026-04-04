from django.urls import path
from . import views

urlpatterns = [
    # 1. Home Page (Root URL)
    path('', views.home, name='home'),

    # 2. About Page 
    path('about/', views.about, name='about'),

    # 3. Shop Page
    path('shop/', views.shop, name='shop'),

    # 4. Create Order 
    path('create_order/<int:product_id>/', views.create_order, name='create_order'),
    
    # 5. My Orders Page 
    path('order/', views.order, name='order'),

    # 6. Admin Dashboard
    path('admin_order/', views.admin_order, name='admin_order'),

    # 7. Order Details & Actions
    path('order/<int:order_id>/', views.detail, name='detail'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/update/', views.update_order, name='update_order'),
    path('order/<int:order_id>/tracking/', views.order_tracker, name='order_tracker'),
    path('order/<int:order_id>/status/', views.status, name='status'),

    # 8. Signup/Logout
    path('accounts/signup/', views.signup, name='signup'),
    
    path('home/', views.home, name='home'),
    
    # === YE LINE ADD KARNA ZARURI HAI ===
    path('dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
]

