import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import Group
from .models import Product, Feedback, Order
from .models import UserProfile # (Ise upar imports ke paas dalna)
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#admin.site.register(UserProfile)

admin.site.site_header = "A1 Bakery Administration"
admin.site.site_title = "A1 Bakery Admin"
admin.site.index_title = "Dashboard"


admin.site.unregister(Group)

# 3. Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag')
    search_fields = ('name',)
    
    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# 4. Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'user')
    list_filter = ('status',)
    search_fields = ('customer_name',)

# 5. FEEDBACK ADMIN (Charts + Read Only) 📊
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating_stars', 'message_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer_name', 'message')
    readonly_fields = ('customer_name', 'email', 'rating', 'message', 'created_at')

    # === YE LINE CHART DIKHAYEGI ===
    change_list_template = "admin/feedback_chart.html"

    # === BUTTONS GAYAB KARNE KA LOGIC ===
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

    # Rating Stars Display
    def rating_stars(self, obj):
        return "⭐" * obj.rating
    rating_stars.short_description = "Rating"

    def message_preview(self, obj):
        return obj.message[:60] + "..." if obj.message else ""

    # === CHART DATA CALCULATION ===
    def changelist_view(self, request, extra_context=None):
        # Good/Medium/Bad count karo
        good = Feedback.objects.filter(rating__gte=4).count()
        medium = Feedback.objects.filter(rating=3).count()
        bad = Feedback.objects.filter(rating__lte=2).count()

        # JSON Data Banao
        chart_data = json.dumps({
            "good": good,
            "medium": medium,
            "bad": bad,
        }, cls=DjangoJSONEncoder)

        extra_context = extra_context or {"chart_data": chart_data}
        return super().changelist_view(request, extra_context=extra_context)
    

# Unregister the default User admin to prevent conflicts
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    Custom UserAdmin to provide a simplified interface.
    Removes unnecessary filters and focuses on essential operations.
    """
    # Define primary columns to display in the list view
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    
    # Disable all sidebar filters for a cleaner UI
    list_filter = []
    
    # Define fields allowed for searching
    search_fields = ('username', 'email')
    
    # Disable the date-based navigation bar
    date_hierarchy = None
    
    # Optional: Disable grouping of actions for a more direct interface
    actions_on_top = True
    actions_on_bottom = False