from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
import しふと

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
      'dates':request.POST['dates'],
      'email':request.POST['email'],
      'message':'Post method!',
    }
    
    #postでくるstr日付をdatetimeに変換して、datesを生成。
    作成日 = しふと.datetime.datetime.strptime(request.POST['dates'],"%Y-%m-%d")
    #月の日付と、休日or平日のリストを取得
    context['message'] = しふと.makeDateSetOfMonth(作成日)
    context['email']  = しふと.makeDaysSetOfMonth(作成日)
    

    return render(request, 'scheduling/result.html',context)

nurse = NurseView.as_view()
