from django.db import models

class ProfilePicture(models.Model):
    original_image = models.ImageField(upload_to='originals/')
    enhanced_image = models.ImageField(upload_to='enhanced/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)