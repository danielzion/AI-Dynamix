from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.db import models
from PIL import Image
from django.contrib.contenttypes.fields import GenericRelation
# from star_ratings.models import Rating

class User(AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('housefinder', 'Housefinder'),
        ('super_admin', 'Super Admin'),
    )
    APPROVAL_CHOICES = (
        ('n', 'Not Requested For Approval'),
        ('p', 'Pending'),
        ('d', 'Request Declined'),
        ('a', 'Verified')
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_CHOICES,
        default='n',
    )
    requested_role = models.CharField(
        choices=REQUESTED_ACCOUNT_TYPE_CHOICES,
        max_length=50,
        default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0]
    )


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.SET_NULL,
        null=True
    )
    profile_picture = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        blank=True,
        null=True
    )
    profile_thumbnail = models.ImageField(
        default='default.png',
        upload_to='profile_pics',
        blank=True,
        null=True
    )
    housefinder_location = models.CharField(max_length=400)
    bio = models.TextField()
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    # ratings = GenericRelation(Rating, related_query_name='profile_ratings')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user}\'s profile'
    
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return 'profile_pics/default.png'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)
        img.save(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (45, 45)
            img.thumbnail(output_size)
            img.save(self.profile_thumbnail.path)
