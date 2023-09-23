from django import forms
from .models import Pictures
from django.forms import modelformset_factory

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Sign Up Form
class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            ]

class MultipleFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        if 'multiple' not in self.attrs:
            self.attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs, renderer)

class PictureForm(forms.ModelForm):
    img = forms.FileField(widget=MultipleFileInput(), required=False, label='Add attachment ')

    class Meta:
        model = Pictures
        fields = ['img']

PictureFormSet = modelformset_factory(Pictures, form=PictureForm, extra=1)
