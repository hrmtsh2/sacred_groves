# forms.py

from django import forms
from .models import PendingSacredGrove

class PendingSacredGroveForm(forms.ModelForm):
    class Meta:
        model = PendingSacredGrove
        fields = [
            'name', 'state', 'district', 'latitude', 'longitude',
            'area_coverage', 'altitude', 'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Devrai Van'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Maharashtra'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Pune'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 18.5204 (Decimal Degrees)',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 73.8567 (Decimal Degrees)',
                'step': 'any'
            }),
            'area_coverage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5 (in Hectares)',
                'step': 'any'
            }),
            'altitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 560 (in Meters)',
                'step': 'any'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide a detailed description of the sacred grove, its significance, any deities associated, flora/fauna observed, etc.'
            }),
            # If you add an image field to your model:
            # 'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'name': 'Name of the Sacred Grove',
            'area_coverage': 'Area Coverage (in Hectares)',
            'altitude': 'Altitude (in Meters above sea level)',
            'latitude': 'Latitude (Decimal Degrees)',
            'longitude': 'Longitude (Decimal Degrees)',
        }

    # Example of custom validation for latitude
    def clean_latitude(self):
        lat = self.cleaned_data.get('latitude')
        if lat is not None and (lat < -90 or lat > 90):
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return lat

    # Example of custom validation for longitude
    def clean_longitude(self):
        lon = self.cleaned_data.get('longitude')
        if lon is not None and (lon < -180 or lon > 180):
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return lon

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)