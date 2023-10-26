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


@login_required(login_url='login')
def DashboardView(request):
    student = request.user.student_user
    tickets = Ticket.objects.filter(student=student).order_by("-created_on")

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
        response['Content-Disposition'] = 'inline; filename="output.pdf"'
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)


