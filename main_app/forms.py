from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

# === SIGNUP FORM  ===
class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full Delivery Address'}), required=True)
    city = forms.CharField(max_length=100, required=True, initial='Malegaon', widget=forms.TextInput(attrs={'placeholder': 'City'}))

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'address', 'city',) 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('quantity',)
        
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }

class OrderTrackerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status', )