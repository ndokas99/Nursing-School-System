from django.urls import path
from accounting import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('record_payment', views.record_payment, name='record_payment'),
    path('download_receipt', views.download_receipt, name='download_receipt'),
    path('record_expenses', views.record_expenses, name='record_expenses'),
    path('display_cashbook', views.display_cashbook, name='display_cashbook'),
    path('display_students', views.display_students, name='display_students'),
]
