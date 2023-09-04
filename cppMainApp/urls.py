from django.contrib import admin
from django.urls import path
from .views import GetAllDataSpecificTable, GetAllTablesNames, UpdateDataSpecificTableViaUniqueIdentification,update_entry

urlpatterns = [
    path('', GetAllTablesNames.as_view()),
    path('table/<str:table_name>/', GetAllDataSpecificTable.as_view()),
    path('update_data_unique_condition/', UpdateDataSpecificTableViaUniqueIdentification.as_view()),
    path('update_row_data',update_entry.as_view(),name='Update_entry')
]
