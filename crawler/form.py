from django import forms
from .models import WantedItem

class WantedItemForm(forms.ModelForm):
    class Meta(object):
        model = WantedItem
        fields = ['base_item', 'upper_price', 'level']
        widgets = {
            'base_item': forms.Select(
                attrs={'class': 'selectpicker form-control',
                        'data-live-search': 'true', }
            ),
            'upper_price': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'level': forms.Select(
                attrs={'class': 'form-control'},
                choices=[(i,i) for i in range(11)],
            ),
        }