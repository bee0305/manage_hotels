from django import forms
from ajax_select.fields import AutoCompleteSelectField
from city.models import City
from .models import Hotel

class CityForm(forms.ModelForm):
    """
    form with optimized input city search instead of dropdown for ADMIN templ in hotel create templ;
    uses autocomplete field == city (module dj-ajax select); see also lookups.py
    """ 
    class Meta:
        model = Hotel
        fields = '__all__'
    
    city = AutoCompleteSelectField('city')

class SearchForm(forms.Form):  
    """
    search form with optimized input city instead of dropdown for templ list of cities;
    uses autocomplete field == city (module dj-ajax select); see also lookups.py
    """  

    city = AutoCompleteSelectField('city',required=False)    
       


