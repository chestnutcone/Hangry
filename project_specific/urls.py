
from django.urls import path
from . import views

urlpatterns = [path('', views.main_view, name='main'),
               path('employee/', views.employee_view, name='employee'),

               ]
