from django.shortcuts import render,redirect
from .models import SchoolFee,Student,Ticket
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib  import messages
from django.contrib.auth import login,logout,authenticate
from .models import FAILED
from django.http import HttpResponse
from datetime import datetime
from django.template import loader
from xhtml2pdf import pisa
import io
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from school.models import Department, Faculty
from app.models import MALE, FEMALE


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.info(request,"Invalid login credentials")
            return redirect("login")
    return render(request, "app/login.html")



def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")

def signup_as_student(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User(username=email, email=email, first_name=first_name, last_name=last_name)
        user.password = make_password(password)
        user.save()

        address = request.POST.get("address")
        picture = request.FILES.get("picture")
        phone = request.POST.get("phone")
        department = request.POST.get("department")
        faculty = request.POST.get("faculty")
        year = request.POST.get("year")
        gender = request.POST.get("gender")
        student = Student(address = address, user=user, image = picture, phone=phone, year = year)
        student.department = Department.objects.get(id=department)
        student.faculty = Faculty.objects.get(id=faculty)
        student.gender = MALE if int(gender) == 0 else FEMALE
        student.save()
        messages.success(request, "student account created successfully")
        return redirect("login")
    
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    context = {
    
        "departments":departments,
        "faculties":faculties
    }
    return render(request,"app/signup.html", context)
    


@login_required(login_url='login')
def DashboardView(request):
    try:
        student = request.user.student_user
        tickets = Ticket.objects.filter(student=student).order_by("-created_on")
    except:
        student = None
        tickets = None
    context = {
        'student':student,
        'tickets': tickets
    }
    return render(request,"app/dashboard.html",context)





@login_required(login_url='login')
def Payment(request):
    fees = SchoolFee.objects.all()
    student = request.user.student_user
    context = {
        'fees':fees
    }
    if request.method == 'POST':
        fee_type = request.POST.get('fees')
        fee = SchoolFee.objects.get(id=fee_type)

        if fee:
            ticket = Ticket.objects.create(
                student = request.user.student_user,
                fee = fee,
                amount = fee.price    
            )
            
            return redirect('confirm-payment',id=ticket.transaction_id)


    return render(request,"app/payments.html",context)


@login_required(login_url='login')
def ConfirmPayment(request,id):
    ticket = Ticket.objects.get(transaction_id = id)
    student = ticket.student

    context = {
        'ticket':ticket,
        'student':student
    }
   
    return render(request,"app/confirm-payment.html",context)


@login_required(login_url='login')
def verify_payment(request, id):
    ticket = get_object_or_404(Ticket, transaction_id=id)
    verified = Ticket.verify_payment(ticket)
    if verified:
        ticket.completed_date = datetime.now()
        ticket.save()

    else:
        ticket.status = FAILED
        ticket.save()
        messages.error(request,"verification failed ")
    return redirect('dashboard')


@login_required(login_url='login')
def Transactions(request):
    tickets = Ticket.objects.filter(student=request.user.student_user)
    context = {
        'tickets':tickets
    }
    return render(request,'app/transactions.html',context)


@login_required(login_url='login')
def transaction_detail(request,id):
    ticket = Ticket.objects.get(transaction_id = id)
    context = {
        'ticket':ticket
    }
    return render(request,'app/transaction-details.html',context)


@login_required(login_url='login')
def payment_slip(request,id):
    ticket = Ticket.objects.get(transaction_id = id)
    context = {
        'ticket':ticket
    }
    return render(request,'app/payment-slip.html',context)

def payment_to_pdf(request,id):
     # Render the HTML content using a Django template
    template = loader.get_template('app/payment-slip.html')
    ticket = Ticket.objects.get(transaction_id = id)
    context = {'ticket':ticket }  # Replace with your data
    html = template.render(context)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="payment_slip_{}.pdf"'.format(id)
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)


