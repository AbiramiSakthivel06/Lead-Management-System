from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lead

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('An account with this username already exists.')

        return cleaned_data


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'company_name',
            'contact_person',
            'mobile_number',
            'email',
            'location',
            'lead_source',
            'status',
            'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs.update({'class': css_class, 'placeholder': f"Enter {field.label}"})
