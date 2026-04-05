from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100) # Tambahkan max_length
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default='REPORTED' # Gunakan kutipan standar
    )
    created_at = models.DateTimeField(auto_now_add=True) # Gunakan huruf kecil agar standar

    def __str__(self):
        return self.title

from django.db.backends.base.base import BaseDatabaseWrapper
BaseDatabaseWrapper.check_database_version_supported = lambda x: None