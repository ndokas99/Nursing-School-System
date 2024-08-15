from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Sum
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from accounting.forms import PaymentForm, ExpenseForm
from accounting.models import Payments, Expenses


def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("/dashboard")
            else:
                return render(request, "login.html", {'error': 'Account is disabled.'})
        else:
            return render(request, "login.html", {'error': 'Invalid credentials entered'})


@login_required
def user_logout(request):
    logout(request)
    return redirect("/user_login")


@login_required
def dashboard(request):
    if list(messages.get_messages(request)):
        return render(request, "dashboard.html")
    messages.info(request, "Welcome to the Dashboard, press any control on the left to start")
    return render(request, "dashboard.html")


@login_required
def record_payment(request):
    request.session.pop('studentName', default=None)
    request.session.pop('studentId', default=None)
    request.session.pop('paymentDate', default=None)
    request.session.pop('level', default=None)
    request.session.pop('amount', default=None)
    request.session['download_receipt'] = "No"

    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            request.session['studentName'] = form.cleaned_data['studentName']
            request.session['studentId'] = form.cleaned_data['studentId']
            request.session['paymentDate'] = form.cleaned_data['paymentDate'].strftime("%d.%m.%Y")
            request.session['level'] = form.cleaned_data['level']
            request.session['amount'] = form.cleaned_data['amount']
            request.session['download_receipt'] = "Yes"

            messages.success(request, "Payment recorded successfully. Receipt downloaded.")
            return redirect("/dashboard")
    else:
        return render(request, "payment.html", {'form': form})


@login_required
def download_receipt(request):
    if request.session['download_receipt'] == "No":
        return HttpResponse("")
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = \
            f"attachment;filename={request.session['studentName']} ({request.session['paymentDate']}).pdf"

        doc = SimpleDocTemplate(response, pagesize=(5.5 * inch, 4.5 * inch))

        table_style = TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('BACKGROUND', (0, 1), (0, -1),  colors.Color(0.106, 0.361, 0.447)),
            ('BACKGROUND', (1, 1), (1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ])

        table = Table([
                [f"Receipt for {request.session['studentName']} as at {request.session['paymentDate']}"],
                ['Student Name', request.session['studentName']],
                ['Student Id', request.session['studentId']],
                ['Level', request.session['level']],
                ['Payment Date', request.session['paymentDate']],
                ['Amount', f"${request.session['amount']}"],
            ],
            style=table_style)

        def page_setup(canvas, doc):
            canvas.saveState()
            canvas.rect(0, 0, 5.5*inch, 4.5*inch)
            canvas.drawImage("static/images/bg.jpg", 0, 0, 5.5 * inch, 4.5 * inch)
            canvas.restoreState()

        doc.build([table], onFirstPage=page_setup, onLaterPages=page_setup)

        return response


@login_required
def record_expenses(request):
    form = ExpenseForm()

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Expenses recorded successfully.")
            return redirect('/record_expenses')
    else:
        return render(request, "expenses.html", {'form': form})


@login_required
def display_cashbook(request):
    dataset = {
        'date': datetime.today().strftime('%d/%m/%Y'),
        'payments': Payments.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'salaries': Expenses.objects.aggregate(Sum('salaries'))['salaries__sum'] or 0,
        'fuel': Expenses.objects.aggregate(Sum('fuel'))['fuel__sum'] or 0,
        'bills': Expenses.objects.aggregate(Sum('bills'))['bills__sum'] or 0,
        'stationery': Expenses.objects.aggregate(Sum('stationery'))['stationery__sum'] or 0,
    }
    dataset['total'] = dataset['salaries']+dataset['fuel']+dataset['bills']+dataset['stationery']
    return render(request, "cashbook.html", context=dataset)


@login_required
def display_students(request):
    students = Payments.objects.all()
    return render(request, 'students.html', context={'students': students.order_by('paymentDate')})
