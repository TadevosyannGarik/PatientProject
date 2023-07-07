from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm
from datetime import datetime
from django.db.models import Q
from django.views.generic import DetailView
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .utils import save_date


def patient_list(request):
    patients = []
    return render(request, 'Patient/patient_list.html', {'patients': patients})


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'Patient/add_patient.html', {'form': form})


def edit_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'Patient/edit_patient.html', {'form': form})


def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()
    return redirect('patient_list')


def search_patients(request):
    query = request.GET.get('q')
    if not query:
        message = 'Введите что-нибудь.'
        return render(request, 'Patient/patient_list.html', {'message': message})
    starts_with_patients = Patient.objects.filter(first_name__istartswith=query) | Patient.objects.filter(
        last_name__istartswith=query)
    contains_patients = Patient.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).exclude(
        id__in=starts_with_patients.values('id'))
    patients = list(starts_with_patients) + list(contains_patients)
    return render(request, 'Patient/patient_list.html', {'patients': patients})


def filter_patients(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not start_date or not end_date:
        message = 'Введите дату.'
        return render(request, 'Patient/patient_list.html', {'message': message})
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d').date()
    patients = Patient.objects.filter(date_added__range=[start_datetime, end_datetime])
    return render(request, 'Patient/patient_list.html', {'patients': patients})


def sort_patients(request):
    field = request.GET.get('field')
    patients = Patient.objects.all().order_by(field)
    return render(request, 'Patient/patient_list.html', {'patients': patients})


def show_all_patient(request):
    patients = Patient.objects.all().order_by("first_name")
    return render(request, 'Patient/all.html', {'patients': patients})


def return_homepage(request):
    return render(request, 'Patient/patient_list.html')

# Найденные пользователи сохраняются в файл
# def search_patients(request):
#     if request.method == 'GET':
#         query = request.GET.get('q', '')
#         patients = Patient.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
#
#         # Формируем данные для файла, например, CSV
#         data = 'First Name,Last Name,Date Added\n'
#         for patient in patients:
#             data += f'{patient.first_name},{patient.last_name},{patient.date_added}\n'
#
#         # Создаем и отправляем файл в ответ на запрос
#         response = HttpResponse(data, content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="patients.csv"'
#         return response
#
#     return render(request, 'your_template.html')


def filter_and_search_patients(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    query = request.GET.get('q')

    patients = Patient.objects.all()

    if start_date and end_date:
        patients = patients.filter(date_added__range=[start_date, end_date])
    elif start_date:
        patients = patients.filter(date_added__gte=start_date)
    elif end_date:
        patients = patients.filter(date_added__lte=end_date)

    if query:
        names = query.split(' ')
        first_name = names[0]
        last_name = names[-1] if len(names) > 1 else ''

        patients = patients.filter(
            Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name)
        )

    return render(request, 'Patient/patient_list.html', {'patients': patients})


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'Patient/patient_detail.html', {"patient": patient})



def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        save_date(first_name, last_name, email, password)
        return redirect('login')
    return render(request, 'Patient/register.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("patient_list")
    return render(request, "Patient/login.html")


def logout(request):
    auth_login(request)
    return redirect('login')




