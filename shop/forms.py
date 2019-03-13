from django import forms
from .models import Product


class SlugProductForm(forms.Form):
    slug = forms.CharField(max_length=150)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Product.objects.filter(slug=slug).count() == 0:
            raise forms.ValidationError("Product does not exist.")
        return slug


class AddProductInCartForm(SlugProductForm):
    quantity = forms.IntegerField()
