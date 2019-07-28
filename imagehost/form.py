from django import forms
from .models import Image

# https://simpleit.rocks/python/django/forms/how-to-use-bootstrap-4-in-django-forms/

# Widgets of django:https://docs.djangoproject.com/en/2.2/ref/forms/widgets/

# select :https://stackoverflow.com/questions/50895806/bootstrap-4-multiselect-dropdown

# set class for 'label' :https://blog.51cto.com/steed/2120211

# https://bootsnipp.com/snippets/eNbOa

# https://stackoverflow.com/questions/48613992/bootstrap-4-file-input-doesnt-show-the-file-name

class ImageCreateForm(forms.ModelForm):

    class Meta(object):
        model=Image
        fields=['title','tags','picture']

        widgets = {
            'title': forms.TextInput(
				attrs={'class': 'form-control'}
				),
            'tags': forms.SelectMultiple(
                attrs={'class': 'selectpicker form-control','data-live-search':'true',}
                ),
            'picture': forms.FileInput(
                attrs={'class': 'custom-file-label'}
                ),
			}
        
