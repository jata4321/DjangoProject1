from django import forms
from .models import Tenor

class CurveForm(forms.ModelForm):

    class Meta:
        model = Tenor
        fields = ['type_name', 'tenor_6m', 'tenor_1y', 'tenor_2y', 'tenor_5y', 'tenor_7y', 'tenor_10y']

        widgets = {
            'type_name': forms.Select(attrs={'class': 'form-control'}),
            'tenor_6m': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenor_1y': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenor_2y': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenor_5y': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenor_7y': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenor_10y': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False
    )