import logging
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Purchase

logger = logging.getLogger(__name__)

def form_view(request):
    if request.method == 'POST':
        vm_name = request.POST.get('vm_name')
        vm_cores = request.POST.get('vm_cores')
        vm_memory = request.POST.get('vm_memory')
        disk_size = request.POST.get('disk_size')

        purchase = Purchase.objects.create(
            vm_name=vm_name,
            vm_cores=vm_cores,
            vm_memory=vm_memory,
            disk_size=disk_size,
        )

        request.session['purchase_id'] = purchase.id

        return redirect('display_view')

    return render(request, 'form.html')

def display_view(request):
    purchase_id = request.session.get('purchase_id')
    if not purchase_id:
        return HttpResponse("No purchase information available")

    purchase = get_object_or_404(Purchase, id=purchase_id)

    context = {
        'vm_name': purchase.vm_name,
        'vm_cores': purchase.vm_cores,
        'vm_memory': purchase.vm_memory,
        'disk_size': purchase.disk_size,
    }
    return render(request, 'display.html', context)

def purchase_select_view(request):
    if request.method == 'GET':
        purchases = Purchase.objects.all()
        return render(request, 'purchase_change_list.html', {'purchases': purchases})

def trigger_jenkins_job(purchase):
    jenkins_url = 'http://192.168.254.158:8080/job/here/buildWithParameters?delay=0sec'
    jenkins_username = 'admin'
    jenkins_token = '11f33e34294718a61eea43e9c6f8af7e10'

    params = {
        'VM_NAME': purchase.vm_name,
        'VM_CORES': purchase.vm_cores,
        'VM_MEMORY': purchase.vm_memory,
        'DISK_SIZE': purchase.disk_size,
    }

    logger.info(f"Triggering Jenkins job with params: {params}")
    response = requests.post(jenkins_url, params=params, auth=(jenkins_username, jenkins_token))
    logger.info(f"Jenkins response status code: {response.status_code}")
    return response.status_code == 201

def trigger_jenkins_build(request):
    purchases = Purchase.objects.filter(is_confirmed=True)
    for purchase in purchases:
        if trigger_jenkins_job(purchase):
            messages.success(request, f"Jenkins job for {purchase.vm_name} triggered successfully.")
        else:
            messages.error(request, f"Failed to trigger Jenkins job for {purchase.vm_name}.")
    return redirect('admin:myform_purchase_changelist')

def admin_confirm_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.is_confirmed = True
    purchase.save()

    if trigger_jenkins_job(purchase):
        messages.success(request, 'Purchase confirmed and Jenkins job triggered successfully.')
    else:
        messages.error(request, 'Purchase confirmed but failed to trigger Jenkins job.')

    return redirect('admin:myform_purchase_changelist')
