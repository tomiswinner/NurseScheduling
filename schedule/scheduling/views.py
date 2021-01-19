from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .forms import TestForm
from .models import Test
import しふと

# Create your views here.


def test(request):
  params = {'message':'','form':None}
  if request.method=='POST':
    form = TestForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/scheduling/hey')
    else:
      params['message'] = '再入力してね'
      params['form'] = form
  else:
    params['form'] = TestForm()
  return render(request,'scheduling/test.html',params)

def hey(request):
  data = Test.objects.all()
  params = {'message':'めんば一覧','data' : data}
  return render(request,'scheduling/hey.html',params)






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


class WorkingTableView(View):
  # def get(self,request,*args,**kwargs):
  def post(self, request,*args,**kwargs):
    context ={
      'dates': request.POST['dates'],
      'datesList' : '',
      }
    
    #postでくるstr日付をdatetimeに変換して、datesを生成。
    作成日 = しふと.datetime.datetime.strptime(request.POST['dates'],"%Y-%m-%d")
    #月の日付と、休日or平日のリストを取得
    context['datesList'] = しふと.makeDateSetOfMonth(作成日)
    # context['email']  = しふと.makeDaysSetOfMonth(作成日)
    return render(request,'scheduling/forWorking.html',context)

WorkingTable = WorkingTableView.as_view()

