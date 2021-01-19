from django.urls import path
from . import views

app_name  ='scheduling'
urlpatterns = [
  path('',views.index,name= 'index'),
  path('nurse/',views.nurse,name='nurse'),
  path('WorkingTable/',views.WorkingTable,name= 'WorkingTable'),
  path('test/',views.test,name = "test"),
  path('hey/',views.hey,name="hey"),
]