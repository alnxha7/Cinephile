from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from datetime import datetime

class User(AbstractUser):
    USER_ROLES = [
        ('critics', 'Critics'),
        ('aspirant', 'Aspirant'),
        ('agency', 'Agency'),
    ]
    mobile = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, blank=True, null=True)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class Movies(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    image = models.ImageField(upload_to='movies/')
    average_rating = models.FloatField(default=0.0)  # Field to store average rating

    def __str__(self):
        return f"{self.title}"

    def update_average_rating(self):
        """Update the average rating for this movie."""
        avg_rating = self.review_set.aggregate(Avg('rating'))['rating__avg']  # Fixed reverse relationship
        self.average_rating = avg_rating/10 if avg_rating is not None else 0.0  # Handle None case
        self.save()
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Override save method to update movie's average rating."""
        super().save(*args, **kwargs)  # Save the review
        self.movie.update_average_rating()

class AspirantPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verification = models.BooleanField(default=False)

    def get_file_type(self):
        extension = self.file.name.split('.')[-1].lower()
        if extension in ['jpg', 'jpeg', 'png', 'gif']:
            return 'image'
        elif extension in ['mp4', 'avi', 'mov']:
            return 'video'
        elif extension in ['doc', 'docx', 'pdf', 'xlsx']:
            return 'document'
        return 'other'
    
class Reactions(models.Model):
    post = models.ForeignKey(AspirantPosts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    is_commented = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically set is_commented based on whether the comment is not blank
        self.is_commented = bool(self.comment and self.comment.strip())
        super().save(*args, **kwargs)