from django.urls import path
from .views import form_view, display_view, purchase_select_view, admin_confirm_purchase, trigger_jenkins_build

urlpatterns = [
    path('', form_view, name='form_view'),
    path('display/', display_view, name='display_view'),
    path('purchases/', purchase_select_view, name='purchase_select_view'),
    path('admin/confirm-purchase/<int:purchase_id>/', admin_confirm_purchase, name='admin_confirm_purchase'),
    path('admin/trigger-jenkins-build/', trigger_jenkins_build, name='trigger_jenkins_build'),
]
