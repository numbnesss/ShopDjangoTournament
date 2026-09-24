from django import forms
from api import models


class BootstrapForm:
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for name, field in self.fields.items():
            field.widget.attrs.pop('maxlength', None)
            field.widget.attrs['class'] = 'form-control is-invalid' if self.errors.get(name) else 'form-control'


class AuthForm(BootstrapForm, forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', 'description']


class ProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'description', 'price', 'image_url', 'category']
        widgets = {'image_url': forms.FileInput()}

    def clean_image_url(self):
        image = self.cleaned_data['image_url']
        if image and hasattr(image, 'content_type'):
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Максимум 2МБ')
            if image.content_type != 'image/jpeg':
                raise forms.ValidationError('Только jpg')
            return image
