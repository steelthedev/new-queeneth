from django.db import models
from django.contrib.auth.models import User
import uuid
from .paystack import PayStack
# Create your models here.
import time
import random
from django.utils.crypto import get_random_string

MALE = "male"
FEMALE = "female"

GENDER_CHOICES = [
    (MALE,"Male"),
    (FEMALE,"Female")
]

PENDING = "pending"
SUCCESS = "success"
FAILED = "failed"

STATUS = [
    (SUCCESS,"Success"),
    (PENDING,"Pending"),
    (FAILED,"Failed")
]

PAYSTACK = "paystack"

PAYMENT = [
    (PAYSTACK,"Payment")
]

def generate_transaction_id():
    timestamp = int(time.time())  # Get the current timestamp as an integer
    random_number = random.randint(1000, 9999)  # Generate a random 4-digit number
    transaction_id = f"{timestamp}{random_number}"  # Combine timestamp and random number
    return transaction_id

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="student_user")
    mat_no = models.CharField(max_length=15)
    year = models.CharField(max_length=200)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    department = models.ForeignKey("school.Department", on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey("school.Faculty", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.user.email
    
    def get_full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.mat_no:
            faculty_code = str(self.faculty.title).upper()[:3] 
            rand_no = get_random_string(7,"123456789")
            self.mat_no = "{}{}".format(faculty_code,rand_no)
        super(Student, self).save(*args, **kwargs)




class SchoolFee(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)


    def __str__(self) -> str:
        return self.title
    


class Ticket(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_ticket")
    fee = models.ForeignKey(SchoolFee, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS, max_length=250,default=PENDING)
    transaction_id = models.CharField(max_length=250)
    payment_mode = models.CharField(choices=PAYMENT,default=PAYSTACK,max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.student.get_full_name()
    
    def save(self, *args, **kwargs):
        id = str(uuid.uuid4)
        print(id)
        if not self.pk:
            self.transaction_id = generate_transaction_id()
        super(Ticket, self).save(*args, **kwargs)

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.transaction_id , self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.status = SUCCESS
            self.save()
        if self.status == SUCCESS:
            return True
        return False