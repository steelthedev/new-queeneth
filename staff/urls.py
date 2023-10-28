from django.urls import path
from . import views

app_name = "staff"


urlpatterns = [
    path('get-all-transactions', views.get_all_payments, name="all-transactions"),
    path('students-list',views.get_all_students, name="all-students"),
    path('add-student', views.add_new_student, name="add-student"),
    path('get-student/<int:id>', views.get_student, name="get-student"),
    path('delete-student/<int:id>', views.delete_student, name="delete-student"),
    path('edit-student-profile/<int:id>', views.edit_student_profile, name="edit-student"),
    path('edit-student-password/<int:id>', views.edit_student_password, name="edit-password"),
    path('edit-basic/<int:id>', views.edit_basic, name="edit-basic"),
    path('add-details', views.add_details, name="add-details"),
    path("add-payment", views.add_payment_type, name="add-payment"),
    path("add-department", views.add_new_deparment, name="add-department"),
    path("add-faculty", views.add_new_faculty, name="add-faculty"),
]