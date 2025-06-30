from django import forms
from .models import MealSlot, Recipe

class MealSlotForm(forms.ModelForm):
    class Meta:
        model = MealSlot
        fields = ['recipe']
        widgets = [
            'recipe': form.Select(attrs=['class': 'form-select'])
        ]