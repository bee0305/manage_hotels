from ajax_select import register, LookupChannel
from .models import City
"""
instaled module (dj-ajax-selects)
if a new hotel object gets created 
instead of drop-down menu with cities|=> input City with jquery selection of entered letter

"""
class CustomLookupChannel(LookupChannel):
    """ default value min_length == 1|=> custom 3 to decrease db hits """
    min_length = 3

    def check_auth(self,request):
        """ default method allows only staff only to search city objects """
        pass    

@register('city')
class CityLookup(CustomLookupChannel):
    model = City
    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='city'>%s</span>" % item.name
