from . import views
from django.urls import path

urlpatterns =[
    path('',views.index,name='Homepage'),
    path('status/<int:id>',views.StatusPage)
]