from django import forms
from .models import Test

class TestForm(forms.ModelForm):
  class Meta:
    model = Test
    fields = ('name','data') #画面に表示するフィールドを指定

