from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="income"),
    path('add_income',views.add_income,name='add-income'),
    path('income-edit/<int:id>',views.Income_edit,name= 'income-edit'),
     path('income-delete/<int:id>',views.Income_delete,name= 'income-delete'),
     path('search-income',csrf_exempt(views.search_income),name= 'search-income'),
     path('income_summary/', views.income_summary,name='income_summary'),
     path('statitics', views.statistics,name='statistics'),
     path('pdf_export', views.pdf_export, name="pdf_export"),
     path('csv_export',views.csv_export, name='csv_export'),
     path("excel_export", views.excel_export,name='excel_export')
]