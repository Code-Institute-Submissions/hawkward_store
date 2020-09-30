from django import forms
from .models import Giftcards, UserProfile


class GiftcardsForm(forms.ModelForm):

    class Meta:
        model = Giftcards
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'email',
            'country', 'street_address', 'city',
            'postcode', 'phone_number',
        )
