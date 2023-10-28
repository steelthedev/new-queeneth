from django.db import models

# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class Faculty(models.Model):
    title = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title