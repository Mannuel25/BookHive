from django.db import models
from users.models import CustomUser

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=25)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    # it can be admin/custom..if it's admin, then the owner would be null
    # else, if it's custom the owner would be populated..just basically to 
    # know which books were uploaded by the admins(or superusers)/normal users
    tag = models.CharField(max_length=6, default="admin")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

