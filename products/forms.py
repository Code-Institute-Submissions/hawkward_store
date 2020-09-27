from django import forms
from .models import ProductsStore, Category, Animals


class ProductsStoreForm(forms.ModelForm):

    class Meta:
        model = ProductsStore
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        animal = Animals.objects.all()
        friendly_names_category = [(c.id, c.get_friendly_name()) for c in categories]
        friendly_names_animals = [(a.id, a.get_friendly_name()) for a in animal]

        self.fields['category'].choices = friendly_names_category
        self.fields['animal'].choices = friendly_names_animals

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class AnimalsForm(forms.ModelForm):

    class Meta:
        model = Animals
        fields = '__all__'
