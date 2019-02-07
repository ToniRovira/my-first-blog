from django import forms
from .models import Peticio,Concesio

from django.forms import ModelForm, DateInput



class PeticioForm(forms.ModelForm):
    class Meta:
        model = Peticio
        fields = ('assistents','data_inici','data_final','motiu','status',)
        widgets = {
          'data_inici': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'data_final': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        
   

    def __init__(self, *args, **kwargs):
        super(PeticioForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['data_inici'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['data_final'].input_formats = ('%Y-%m-%dT%H:%M',)
'''
vell
class ConcesioForm(forms.ModelForm):
    class Meta:
        model = Concesio
        fields = ('sala_donada','start_time','end_time',)
'''

class ConcesioForm(ModelForm):
  class Meta:
    model = Concesio
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    #fields = '__all__'
    fields = ('sala_donada','start_time','end_time',)

  def __init__(self, *args, **kwargs):
    super(ConcesioForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
