from django import forms
from .models import Pictures

from django.forms import modelformset_factory


class PictureForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ['img']
PictureFormSet = modelformset_factory(Pictures, form=PictureForm, extra=1)
