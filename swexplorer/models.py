from django.db import models


class Collection(models.Model):
    filename = models.CharField(max_length=32)
    total_items = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
