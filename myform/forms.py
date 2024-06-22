# MyForm/forms.py

from django import forms
from .models import Purchase

class VMForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['vm_name', 'vm_cores', 'vm_memory', 'disk_size']
