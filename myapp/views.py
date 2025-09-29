from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponse
from django.db.models import Count
from django.utils.timezone import now
from datetime import date



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def gallery(request):
    return render(request, 'gallery.html')

def team(request):
    return render(request, 'team.html')



def blog(request):
    return render(request, 'blog.html')

def blog_details(request):
    return render(request, 'blog_details.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):

    if request.method=="POST":

        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "Email Already Exists"
            return render(request, 'signup.html',{'msg':msg})
        
        except:

            if request.POST['password'] == request.POST['cpassword']:

                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    role = request.POST['role'],
                    photo = request.FILES['photo'],
                    password = request.POST['password'],
                )

                msg = "Sign-Up SuccessFully"
                return render(request, 'login.html',{'msg':msg})
            else:
                msg = "Password And Conform Password Doesn't Match"
                return render(request, 'signup.html',{'msg':msg})
    else:
        return render(request, 'signup.html')

def login(request):
    
    if request.method=="POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email']=user.email
                request.session['role']=user.role
                request.session['photo']=user.photo.url
                request.session['user_id']=user.id


                if user.role == "patient":
                    return redirect('index')
                elif user.role == "doctor":
                    return redirect('dindex')
                elif user.role == "admin":
                    return redirect('admin_dashboard')

            
            else:
                msg = "Password Doesn't Match"
                return render(request, 'login.html',{'msg':msg})
        except:
            msg = "Email Is Not Register"
            return render(request, 'login.html',{'msg':msg})
    else:
        return render(request, 'login.html')



def logout(request):
    request.session.flush()  
    return redirect('login')  

def fpass(request):

    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp = random.randint(1001,9999)
            subject = 'OTP For Forget Password '
            # message = "HI"+user.name+"Your Otp Is : --> ",+str(otp)
            message = "HI " + user.name + " Your OTP is: --> " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recepent_list = [user.email,]
            send_mail(subject,message,email_from,recepent_list)
            request.session['email']=user.email
            request.session['otp']=otp
            return render(request, "otp.html")
        except:
            msg = "Email Doesn't Exists"
            return render(request, 'fpass.html',{'msg':msg})

    else:
        return render(request, 'fpass.html')
        


def changepass(request):

    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":

        if user.password==request.POST['opassword']:
            if request.POST['npassword'] == request.POST['cpassword']:
                user.password=request.POST['npassword']
                user.save()
                return redirect('profile')
            
            else:
                msg = "New Password Or Conform Password Doesn'y Match"
                return render(request, 'changepass.html',{'msg':msg})

        else:
            msg="Old Password Doesn't match!!"            
            return render(request, 'changepass.html',{'msg':msg})
        
    else:
        return render(request, 'changepass.html')



def otp(request):

    if request.method=="POST":
        try:

            otp = int(request.session['otp'])
            uotp = int(request.POST.get('uotp'))

            # uotp = int(request.POST.get['uotp'])

            if otp == uotp:
                del request.session['otp']
                return render(request, "newpass.html")
            else:
                msg = "Otp Doesn't Match"
                return render(request, "otp.html",{'msg':msg})
            
        except Exception as e:
            print("Error in OTP view:", e)  
            msg = "Something went wrong. Please try again."
            return render(request, "otp.html", {'msg': msg})

        
    else:
        return render(request, 'otp.html')

def newpass(request):

    if request.method=="POST":
        try:
            user=User.objects.get(email=request.session['email'])

            if request.POST['npassword'] == request.POST['cpassword']:
                user.password = request.POST['npassword']
                user.save()
                del request.session['email']
                return redirect('login')
            
            else:
                msg = "Password And Correct Password  Doesn't Matches"
                return render(request, 'newpass.html',{'msg':msg})
            
        except:
            pass

    else:
        return render(request, 'newpass.html')


def dindex(request):
    return render(request, 'dindex.html')



def profile(request):
    email = request.session.get('email')

    if not email:
        return redirect('login')  

    user = User.objects.get(email=email) 
    return render(request, 'profile.html', {'user': user})  

 
def d_profile(request):
    email = request.session.get('email')

    if not email:
        return redirect('login')  

    user = User.objects.get(email=email)  
    return render(request, 'd_profile.html', {'user': user})  


def appointment(request):
    doctors = User.objects.filter(role="doctor")


    if request.method=="POST":
        pname=request.POST.get('pname')
        # pemail=request.POST.get('pemail')
        department=request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        pphone = request.POST.get('pphone')
        date=request.POST.get('date')
        message=request.POST.get('message')

        try:
            doctor = User.objects.get(id=doctor_id,role="doctor")
            patient_user = User.objects.get(id=request.session['user_id'])

            Appointment.objects.create(
                patient=patient_user,
                pname=pname,
                pemail=patient_user.email,
                department=department,
                doctor=doctor,
                pphone=pphone,
                date=date,
                message=message
            )

            msg = "Appointment Submited"
            return render(request, "appointment.html",{'doctors': doctors, 'msg': msg})
        
        except User.DoesNotExist:
            msg = "Doctor not found"
            return render(request, "appointment.html", {'doctors':doctors, 'msg':msg})

    else:
        return render(request,"appointment.html",{'doctors':doctors})



def history(request):
    user = User.objects.get(email=request.session['email'])
    appointments = Appointment.objects.filter(pemail=user.email).order_by('-date')  # latest first
    return render(request, 'history.html', {'appointments': appointments})




def d_dash(request):
    if 'user_id' not in request.session or request.session['role'] != 'doctor':
        return redirect('login')

    doctor_id = request.session['user_id']
    doctor = User.objects.get(id=doctor_id)

    appointments = Appointment.objects.filter(doctor_id=doctor_id)

    return render(request, "d_dash.html", {"doctor": doctor, "appointments": appointments})

def update_appointment(request, pk, action):
    appointment = Appointment.objects.get(id=pk)
    if action == "approve":
        appointment.status = "approved"
    elif action == "reject":
        appointment.status = "rejected"
    appointment.save()
    return redirect("d_dash")


def delete_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
        appointment.delete()
        return redirect("d_dash") 
    except Appointment.DoesNotExist:
        return redirect("d_dash") 
    


def upload_record(request, patient_id):
    if request.session['role'] != "doctor":
        return redirect("login")  

    patient = User.objects.get(id=patient_id, role="patient")

    if request.method == "POST":
        description = request.POST.get("description")
        file = request.FILES.get("file")

        MedicalRecord.objects.create(
            patient=patient,
            doctor=User.objects.get(id=request.session['user_id']),
            description=description,
            file=file
        )
        msg = "Record uploaded successfully"
        return render(request, "upload_record.html", {"patient": patient, "msg": msg})

    return render(request, "upload_record.html", {"patient": patient})


def my_records(request):
    if request.session['role'] != "patient":
        return redirect("login")

    user = User.objects.get(id=request.session['user_id'])
    records = MedicalRecord.objects.filter(patient=user).order_by('-created_at')
    return render(request, "my_records.html", {"records": records})


def admin_dashboard(request):
    if request.session.get('role') != "admin":
        return redirect("login")

    today = date.today()  

    
    total_doctors = User.objects.filter(role="doctor").count()
    total_patients = User.objects.filter(role="patient").count()
    total_appointments = Appointment.objects.count()


    today_appointments = Appointment.objects.filter(date=today).count()

  
    today_patients = User.objects.filter(role="patient", created_at__date=today).count()

  
    last7days = (
        Appointment.objects
        .extra({'day': "date(date)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    doctors = User.objects.filter(role="doctor")
    patient = User.objects.filter(role="patient")
    appointments = Appointment.objects.all().order_by('-date')
    context = {
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "today_appointments": today_appointments,
        "today_patients": today_patients,
        "last7days": last7days,
        "doctors": doctors,
        "patient":patient,
        "appointments":appointments,
    }
    return render(request, "admin_dashboard.html", context)

def delete_doctor(request, pk):
    try:
        doctor = User.objects.get(id=pk, role="doctor")
        doctor.delete()
        return redirect("admin_dashboard")
    except User.DoesNotExist:
        return redirect("admin_dashboard")


def adelete_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
        appointment.delete()
        return redirect("admin_dashboard") 
    except Appointment.DoesNotExist:
        return redirect("admin_dashboard") 

def apatientsdelete(request, pk):
    try:
        patient = User.objects.get(id=pk, role="patient")
        patient.delete()
        return redirect("admin_dashboard")
    except User.DoesNotExist:
        return redirect("admin_dashboard")

def alogout(request):
    request.session.flush()  
    return redirect('login')