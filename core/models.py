from django.db import models
from user.models import User
from ckeditor.fields import RichTextField

class OpenAICommand(models.Model):
    CATEGORY_CHOICES = [
        ('Code Review', 'Code Review'),
        ('Automate', 'Automate'),
        ('Tester', 'Tester'),
    ]

    title = models.CharField(max_length=255)
    prompt = RichTextField()
    response = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    version = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.date}"