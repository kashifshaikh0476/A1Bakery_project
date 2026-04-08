import os
import qrcode
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F 
from .models import Order, Map, Product, Feedback, UserProfile 
from .forms import OrderForm, OrderTrackerForm, CustomUserCreationForm 
from django.utils import timezone
from django.http import JsonResponse 
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from django.http import HttpResponse
from .models import Order


def create_admin(request):
    user, created = User.objects.get_or_create(username='kashif')
    user.set_password('kashif047') # Ekdum simple password rakha hai testing ke liye
    user.is_superuser = True
    user.is_staff = True
    user.save()
    if created:
        return HttpResponse("New Admin 'kashif' created ✅")
    else:
        return HttpResponse("Admin 'kashif' password updated to 'kashif047' 🔄")


def generate_upi_qr(amount, order_id):
    upi_id = "8421857457@ybl" 
    name = "A1%20Bakery"
    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn=Order_{order_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- AUTHENTICATION ---
def custom_logout(request):
    logout(request)
    return redirect('home')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            
            profile = UserProfile.objects.get(user=user)
            profile.phone = form.cleaned_data.get('phone')
            profile.address = form.cleaned_data.get('address')
            profile.city = form.cleaned_data.get('city')
            profile.save()
            
            login(request, user)
            return redirect('/order/')
        else:
            error_message = 'Invalid sign up - please check the errors below.'
    else:
        form = CustomUserCreationForm() 
        
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})

# --- PUBLIC PAGES ---
def home(request):
    return render(request, 'home.html')

def about(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        msg = request.POST.get('message')
        stars = request.POST.get('rating')
        if name and stars: 
            Feedback.objects.create(customer_name=name, message=msg, rating=stars)
        return redirect('about') 
    return render(request, 'about.html')

def shop(request):
    products = Product.objects.all() 
    return render(request, 'shop.html', {'products': products})

# --- ORDER MANAGEMENT ---
@login_required
def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            
            # === MAGIC: AUTO-FILL FROM USER PROFILE ===
            order.customer_name = request.user.username
            
            if hasattr(request.user, 'userprofile'):
                order.customer_phone = request.user.userprofile.phone or ""
                order.address = request.user.userprofile.address or ""
                order.city = request.user.userprofile.city or ""
            # ==========================================

            pay_method = request.POST.get('payment_type') 
            trans_id = request.POST.get('transaction_id')

            if pay_method == 'online' and (not trans_id or len(trans_id) < 12):
                return render(request, 'order/create_order.html', {
                    'form': form, 'product': product, 'error': '12-digit Transaction ID is required!'
                })

            order.transaction_id = trans_id
            order.save()
            return redirect('detail', order_id=order.id) 
    
    return render(request, 'order/create_order.html', {'form': form, 'product': product})
@login_required
def detail(request, order_id):
    found_order = Order.objects.get(id=order_id)
    order_tracker = OrderTrackerForm()
    total_amount = found_order.product.price * found_order.quantity
    qr_code = generate_upi_qr(total_amount, found_order.id)
    
    return render(request, 'order/order_detail.html', {
        'order': found_order, 'order_tracker': order_tracker, 'qr_code': qr_code, 'total_amount': total_amount
    })

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request,'order/order.html', {'orders': orders})

@login_required
def delete_order(request, order_id):
    order_obj = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order_obj.status == 'Pending':
        order_obj.delete()
    else:
        # if admin changed the status
        pass 
        
    return redirect('order')

@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        return render(request, 'order/update_order.html', {'form': form})
    else: 
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order=form.save()
            return redirect('detail', order_id=order.id)

# --- ADMIN DASHBOARD ---
@user_passes_test(lambda u: u.is_superuser) 
def admin_order(request):
    orders = Order.objects.all().order_by('-id')
    total_orders = orders.count()
    pending_count = Order.objects.filter(status='Pending').count()
    
    time_filter = request.GET.get('filter', 'all')
    now = timezone.now()
    
    if time_filter == 'today':
        revenue_orders = Order.objects.filter(created_at__date=now.date())
        rev_label = "TODAY'S REVENUE"
    elif time_filter == 'month':
        revenue_orders = Order.objects.filter(created_at__year=now.year, created_at__month=now.month)
        rev_label = "THIS MONTH'S REVENUE"
    elif time_filter == 'year':
        revenue_orders = Order.objects.filter(created_at__year=now.year)
        rev_label = "THIS YEAR'S REVENUE"
    else:
        revenue_orders = Order.objects.all()
        rev_label = "TOTAL REVENUE"
        
    revenue_data = revenue_orders.aggregate(total=Sum(F('product__price') * F('quantity')))
    revenue = revenue_data['total'] if revenue_data['total'] else 0

    return render(request,'order/admin_dashboard.html', {
        'orders': orders, 
        'total_orders': total_orders, 
        'pending_count': pending_count, 
        'revenue': revenue,
        'rev_label': rev_label,
        'active_filter': time_filter
    })

def status(request, order_id):
    found_order = Order.objects.get(id=order_id)
    get_status = request.POST.get('status')
    if get_status:
        found_order.status = get_status
        found_order.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page if previous_page else 'detail', order_id=order_id)

@login_required
def order_tracker(request, order_id):
    form = OrderTrackerForm(request.POST)
    if form.is_valid():
        new_tracking = form.save(commit=False)
        new_tracking.order_id = order_id
        new_tracking.save()
    return redirect('detail', order_id=order_id)

def map_display(request):
    try:
        map = Map.objects.first() 
    except:
        map = None
    return render(request, 'about')

def dashboard_stats_api(request):
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    
    # Base queryset for filtering
    orders = Order.objects.all()
    
    if filter_type == 'today':
        orders = orders.filter(created_at__date=now.date())
    elif filter_type == 'month':
        orders = orders.filter(created_at__year=now.year, created_at__month=now.month)
    elif filter_type == 'year':
        orders = orders.filter(created_at__year=now.year)

    # Use the same revenue logic as your admin_order view
    revenue_data = orders.aggregate(total=Sum(F('product__price') * F('quantity')))
    revenue = revenue_data['total'] if revenue_data['total'] else 0

    data = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='Pending').count(),
        'total_revenue': revenue
    }
    return JsonResponse(data)



def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="A1_Bakery_Statement.csv"'

    writer = csv.writer(response)
    # Headings
    writer.writerow(['Order ID', 'Customer Name', 'Product', 'Quantity', 'Status', 'Date'])

    orders = Order.objects.all().order_by('-created_at')

    for order in orders:
        order_date = order.created_at.strftime('%d-%m-%Y %H:%M') if order.created_at else "N/A"
        
        writer.writerow([
            order.id, 
            order.customer_name, 
            order.product.name if order.product else "No Product", 
            order.quantity, 
            order.status, 
            order_date
        ])

    return response


from django.template.loader import get_template
from xhtml2pdf import pisa

def export_orders_pdf(request):
    orders = Order.objects.all().order_by('-created_at')
    template_path = 'admin_orders_pdf.html' 
    context = {'orders': orders}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="A1_Bakery_Report.pdf"'
    
    # HTML ko PDF convert
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response