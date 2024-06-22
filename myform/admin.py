from django.contrib import admin
from django.contrib import messages
from .models import Purchase
import requests

def trigger_jenkins_job(purchase):
    jenkins_url = 'http://192.168.254.158:8080/job/here/buildWithParameters?delay=0sec'
    jenkins_username = 'admin'
    jenkins_token = '11f33e34294718a61eea43e9c6f8af7e10'  # Replace with your actual token

    params = {
        'VM_NAME': purchase.vm_name,
        'VM_CORES': purchase.vm_cores,
        'VM_MEMORY': purchase.vm_memory,
        'DISK_SIZE': purchase.disk_size,
    }

    response = requests.post(jenkins_url, params=params, auth=(jenkins_username, jenkins_token))
    return response.status_code == 201

def build_purchase_vm(modeladmin, request, queryset):
    for purchase in queryset:
        if purchase.is_confirmed:
            if trigger_jenkins_job(purchase):
                messages.success(request, f"Jenkins job for {purchase.vm_name} triggered successfully.")
            else:
                messages.error(request, f"Failed to trigger Jenkins job for {purchase.vm_name}.")
        else:
            messages.error(request, f"Purchase {purchase.vm_name} is not confirmed yet.")

build_purchase_vm.short_description = "Trigger Jenkins build for selected purchases"

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('vm_name', 'vm_cores', 'vm_memory', 'disk_size', 'is_confirmed')
    actions = [build_purchase_vm]

    def save_model(self, request, obj, form, change):
        if obj.is_confirmed and change:
            if trigger_jenkins_job(obj):
                messages.success(request, f"Jenkins job for {obj.vm_name} triggered successfully.")
            else:
                messages.error(request, f"Failed to trigger Jenkins job for {obj.vm_name}.")
        super().save_model(request, obj, form, change)

admin.site.register(Purchase, PurchaseAdmin)
