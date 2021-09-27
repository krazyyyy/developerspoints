from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(null=True, blank=True)
    attrs = RichTextField(null=True, blank=True)
    PORTFOLIO_TYPE = (
        ("Web Development", "Web Development"),
        ("Scripting", "Scripting"),
        ("Other", "Other"),
    )
    project_type = models.CharField(max_length=64, default="Other", choices=PORTFOLIO_TYPE)
    image = models.ImageField(upload_to="media/portfolio", null=True, blank=True)

class ProjectImages(models.Model):
    project = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="project_picture")
    heading = models.CharField(max_length=64)
    image = models.ImageField(upload_to="media/projects")
    responsive = models.BooleanField(default=False)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.ForeignKey('EmailLists', on_delete=models.CASCADE, related_name="emails")
    message = RichTextField()
    contacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} messaged at {self.contacted_at}"


class EmailLists(models.Model):
    email = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.email}"