# views.py
from django.shortcuts import render, redirect
from .models import VMPurchaseRequest

def confirm_purchase(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        action = request.POST.get('action')
        if action == 'confirm':
            # Confirm purchase logic
            purchase = Purchase.objects.get(pk=purchase_id)
            purchase.confirmed = True
            purchase.save()
            # Redirect to admin interface or another page
            return redirect('admin:app_purchase_changelist')
        elif action == 'deny':
            # Deny purchase logic
            purchase = Purchase.objects.get(pk=purchase_id)
            purchase.delete()  # Or mark as denied
            # Redirect to admin interface or another page
            return redirect('admin:app_purchase_changelist')
    return render(request, 'confirmation.html')
