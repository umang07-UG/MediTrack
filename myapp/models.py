from django.db import models

# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile = models.BigIntegerField()
    role=models.CharField(max_length=20,default="patient")
    photo=models.ImageField(default="",upload_to="user_photo")
    password=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}  ,  {self.role}"
    

class Appointment(models.Model):
    dep = (
        ("diagnostic","diagnostic"),
        ("psychological","psychological"),
        ("therapy","therapy"),
        ("counseling","counseling"),
    )


    pname = models.CharField(max_length=100)
    pemail = models.EmailField()
    department = models.CharField(max_length=52,choices=dep)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    pphone = models.BigIntegerField()
    date = models.DateField()
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending","Pending"), ("approved","Approved"), ("rejected","Rejected")],
        default="pending"
    )
