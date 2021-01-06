from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from . import testes1
# Create your views here.


def index(request):
  context = {}
  template = loader.get_template('scheduling/index.html')
  return HttpResponse(template.render(context,request))

class NurseView(View):
  def get(self, request,*args,**kwargs):
    context= {
      'message':"Get mehod HOO!",
    }
    return render(request,'scheduling/index.html',context)
  
  def post(self,request,*args,**kwargs):
    context ={
      'name':request.POST['name'],
      'email':request.POST['email'],
      'message':'Post method!'
    }
    context['name'] = context['name'] + 'ひゃっはーなっしー'
    
    return render(request, 'scheduling/index.html',context)

nurse = NurseView.as_view()
