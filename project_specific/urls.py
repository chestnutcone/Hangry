
from django.urls import path
from . import views

urlpatterns = [path('', views.main_view, name='main'),
               path('setting/', views.setting_view, name='setting'),
               path('employee/', views.employee_view, name='employee'),
               path('employee/history', views.employee_history_view, name='employee_history'),
               path('employee/export_transaction_history/<str:start_date>/<str:end_date>/',
                    views.employee_transaction_history_download_view, name='employee_transaction_history'),
               path('manager/', views.manager_view, name='manager'),
               path('manager/export_order_history/<str:start_date>/<str:end_date>/',
                    views.manager_download_view, name='manager_download_csv'),
               path('manager/people', views.manager_people_view, name='manager_people'),
               ]
