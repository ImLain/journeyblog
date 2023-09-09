from django import forms
from .models import Pictures
from django.forms import modelformset_factory

class MultipleFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        if 'multiple' not in self.attrs:
            self.attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs, renderer)

class PictureForm(forms.ModelForm):
    img = forms.FileField(widget=MultipleFileInput(), required=False)

    class Meta:
        model = Pictures
        fields = ['img']

PictureFormSet = modelformset_factory(Pictures, form=PictureForm, extra=1)
