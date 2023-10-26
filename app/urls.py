from django.urls import path

from . import views

urlpatterns = [
    path('', views.LoginView, name="login"),
    path('dashboard',views.DashboardView, name="dashboard"),
    path('make-payments',views.Payment, name="make-payments"),
    path('confirm-payment/<str:id>',views.ConfirmPayment, name="confirm-payment"),
    path('verify-payment/<str:id>',views.verify_payment, name="verify-payment"),
    path('transactions',views.Transactions, name="transactions"),
    path('logout', views.LogoutView, name="logout"),
    path('transaction-detail/<int:id>', views.transaction_detail, name="transaction-detail"),
    path('payment-slip/<int:id>', views.payment_slip, name="payment-slip"),
    path('print-payment/<int:id>', views.payment_to_pdf, name="print-payment")

    
]