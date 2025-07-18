# core/models.py
from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5) # 1 to 5 stars
    content = models.TextField()
    service = models.CharField(max_length=100, blank=True, null=True)
    approved = models.BooleanField(default=False) # This is the crucial field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Testimonial by {self.name} (Approved: {self.approved})"

    class Meta:
        ordering = ['-created_at'] # Order by latest created first
