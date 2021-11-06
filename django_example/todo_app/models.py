from django.db import models


# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    due_date = models.DateTimeField()
    done = models.BooleanField(default=False)
