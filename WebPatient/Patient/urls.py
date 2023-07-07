from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('patient/list', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patients/search/', views.search_patients, name='search_patients'),
    path('patients/filter/', views.filter_patients, name='filter_patients'),
    path('patients/all/', views.show_all_patient, name="all"),
    path('filter/', views.filter_and_search_patients, name='filter_and_search_patients'),
    path('patient/detail/<int:pk>', views.patient_detail, name='patient_detail')
]
