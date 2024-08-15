from django import forms
from accounting.models import *


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'
        widgets = {
            'paymentDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
        }
        labels = {
            'paymentDate': 'Payment Date',
            'amount': 'Amount',
            'studentName': 'Student Name',
            'studentId': 'Student ID',
            'level': 'Level'
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fuel': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
            'stationery': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
            'bills': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
            'salaries': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
        }
        labels = {
            'date': 'Date',
            'fuel': 'Fuel',
            'stationery': 'Stationery',
            'bills': 'Bills',
            'salaries': 'Salaries'
        }
