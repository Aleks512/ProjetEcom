from django import forms
from .models import Category, Product, Order, Comment


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('Cette catégorie existe déjà.')
        return name


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Cette catégorie existe déjà.')
        return name


class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []

# --------------- Products---------------------------
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'unit_price', 'stock', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError('Ce produit existe déjà.')
        return name


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'unit_price', 'stock', 'category', 'image']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Ce produit existe déjà.')
        return name

class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = []

# ------------ Orders --------------------
class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'quantity')

class OrderDeleteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'