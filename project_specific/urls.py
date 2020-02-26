
from django.urls import path
from . import views

urlpatterns = [path('', views.main_view, name='main'),
               path('employee/', views.employee_view, name='employee'),
               path('manager/', views.manager_view, name='manager'),
               path('manager/export_csv/<str:start_date>/<str:end_date>/',
                    views.manager_download_view, name='manager_download_csv'),
               path('manager/people', views.manager_people_view, name='manager_people'),
               ]
