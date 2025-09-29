from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):

    ROLES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    )

    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile = models.BigIntegerField()
    role = models.CharField(max_length=20, choices=ROLES, default="patient")
    photo=models.ImageField(default="",upload_to="user_photo")
    password=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}  ,  {self.role}"
    

class Appointment(models.Model):
    dep = (
        ("diagnostic","diagnostic"),
        ("psychological","psychological"),
        ("therapy","therapy"),
        ("counseling","counseling"),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        null=True, 
        blank=True,
        related_name="appointments"
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



class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records_as_patient", limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records_as_doctor", limit_choices_to={'role': 'doctor'})
    file = models.FileField(upload_to="records/")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} ({self.created_at.date()})"
