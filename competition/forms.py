from django import forms
from .models import *
from multiupload.fields import MultiFileField


# create forms  

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'car_model', 
            'car_brand', 
            'description', 
            'specifications',  
            'image', 
            'ticket_price', 
            'total_tickets', 
            'start_date', 
            'end_date', 
            'max_entries_per_user',
        ]

        start_date  = forms.DateTimeField(
            input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
            ],
            required=False
        )

        end_date  = forms.DateTimeField(
            input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
            ],
            required=False
        )
        

class CompetitionImageForm(forms.ModelForm):
    images = MultiFileField(required=False)

    class Meta:
        model = CompetitionImage
        fields = ['image']