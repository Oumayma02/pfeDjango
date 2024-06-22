# purchases/models.py
from django.db import models

class VMPurchaseRequest(models.Model):
    vm_name = models.CharField(max_length=100)
    vm_cores = models.IntegerField()
    vm_memory = models.IntegerField()
    disk_size = models.IntegerField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.vm_name
