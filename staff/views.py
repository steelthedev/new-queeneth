from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect

# Create your views here.
from .models import Staff

from .decorators import staff_required
from app.models import Ticket,Student,SchoolFee
from school.models import Department, Faculty
from django.contrib.auth.hashers import make_password
from app.models import MALE,FEMALE
from django.contrib.auth.models import User
from django.contrib import messages

@staff_required
def get_all_students(request):
    students = Student.objects.all()
    context = {
        "students":students
    }

    return render(request,"staff/students-list.html",context)

@staff_required
def get_student(request,id):
    student = Student.objects.get(id=id)
    tickets = Ticket.objects.filter(student=student)
    context = {
        "student":student,
        'tickets':tickets
    }

    return render(request, "staff/student-profile.html", context)

@staff_required
def delete_student(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("staff:all-students")
    

@staff_required
def block_student(request,id):
    student = Student.objects.get(id=id)
    student.is_active = False
    student.save

@staff_required
def get_all_payments(request):
    ticket = Ticket.objects.all()
    context = {
        "tickets":ticket
    }
    return render(request,"staff/transactions-list.html", context)

@staff_required
def get_student_payments(request,id):
    student = Profile.objects.get(id=id)
    transactions = Transaction.objects.filter(user = student )
    context = {
        "transactions":transactions
    }
    return render(request,"dashboard/transaction-history.html", context)


@staff_required
def edit_student_profile(request,id):
    student = Student.objects.get(id=id)
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    context ={
        "student":student,
        "faculties":faculties,
        "departments":departments
    }
    return render(request,"staff/edit-student-profile.html",context)


@staff_required
def add_new_student(request):

    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            user = User(username=email, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()

            address = request.POST.get("address")
            picture = request.FILES.get("picture")
            phone = request.POST.get("phone")
            department = request.POST.get("department")
            faculty = request.POST.get("faculty")
            year = request.POST.get("year")
            gender = request.POST.get("gender")
            print(department, faculty)
            student = Student(address = address, user=user, image = picture, phone=phone, year = year)
            student.department = Department.objects.get(id=department)
            student.faculty = Faculty.objects.get(id=faculty)
            student.gender = MALE if int(gender) == 0 else FEMALE
            student.save()
            messages.success(request, "student added successfully")
            return redirect("staff:add-student")
        except Exception as e:
            print(str(e))
            messages.warning(request, "student could not be added")
            return redirect("staff:add-student")

    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    context = {
    
        "departments":departments,
        "faculties":faculties
    }
    return render(request, "staff/add-student.html",context)

def add_details(request):
    return render(request, "staff/add-details.html")

@staff_required
def add_payment_type(request):
    if request.method == "POST":

        title = request.POST.get("title")
        price = request.POST.get("price")

        SchoolFee.objects.create(title=title, price=price)
        return redirect("staff:add-details")

def add_new_faculty(request):
    if request.method == "POST":
        title = request.POST.get("title")

        Faculty.objects.create(title=title)
        return redirect("staff:add-details")

def add_new_deparment(request):

    if request.method == "POST":
        title = request.POST.get("title")

        Department.objects.create(title=title)
        return redirect("staff:add-details")
    



@staff_required
def edit_student_password(request,id):

    if request.method == "POST":
        student = Student.objects.get(id=id)
        new_password = request.POST.get("new_password")

        student.user.password = make_password(new_password)
        student.user.save()
        return redirect("staff:edit-student",student.id)
    
@staff_required
def edit_basic(request,id):
    if request.method == "POST":
        student = Student.objects.get(id=id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        faculty  = request.POST.get("faculty")
        department = request.POST.get("department")

        faculty_object = Faculty.objects.get(id=faculty)
        department_object = Department.objects.get(id=department)
        student.user.first_name = first_name
        student.user.last_name = last_name
        student.faculty = faculty_object
        student.department = department_object
        student.user.save()
        student.save()

        return redirect("staff:edit-student", student.id)        



