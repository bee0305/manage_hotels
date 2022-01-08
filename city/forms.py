from django import forms
from ajax_select.fields import AutoCompleteSelectField
from .models import Hotel



# class BaseForm(forms.ModelForm):
#     """ base for any model-form with bootstrap classes"""
#     class Meta:
#         model = None 
#         fields = None

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
            


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name','unid')
        labels = {'name': 'Enter a name','unid':'Enter a unid'}
        

class CityForm(forms.ModelForm):
    """
    form for admin tempate create hotel object: city easy search via ajax instead instead of (large) dropdown;
    uses autocomplete field == city (package: dj-ajax select); see also lookups.py
    """

    class Meta:
        model = Hotel
        fields = '__all__'

    city = AutoCompleteSelectField('city')


class SearchForm(forms.Form):
    """
    for all cities template: easy search via ajax;
    uses autocomplete field == city (package: dj-ajax select); see also lookups.py
    """

    city = AutoCompleteSelectField('city', required=False)

