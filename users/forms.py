from django import forms
from .models import Giftcards

class GiftcardsForm(forms.ModelForm):

    class Meta:
        model = Giftcards
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)