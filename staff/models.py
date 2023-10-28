from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_user" )
    faculty = models.ForeignKey("school.Faculty", on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey("school.Department", on_delete=models.SET_NULL, null=True)
    staff_id = models.CharField(max_length=300)
    phone = models.CharField(max_length=200)
    image = models.FileField(null=True, blank=True)
    about = models.TextField()
    expertise = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.email
    