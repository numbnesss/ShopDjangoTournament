from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, DetailView

from api import models
from . import forms
from .utils import make_watermarked_thumbnail


class AdminOnly:
    def dispatch(self, req, *a, **kw):
        if not (req.user.is_authenticated and req.user.is_staff):
            return redirect('ad:auth')
        return super().dispatch(req, *a, **kw)


class Auth(FormView):
    template_name = 'login.html'
    form_class = forms.AuthForm
    success_url = reverse_lazy('ad:categories')

    def dispatch(self, req, *a, **kw):
        if req.user.is_authenticated and req.user.is_staff:
            return redirect('ad:categories')
        return super().dispatch(req, *a, **kw)

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user is None or not user.is_staff:
            form.add_error(None, 'Неверный email или пароль')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class Logout(View):
    def post(self, req):
        logout(req)
        return redirect('ad:auth')


class Categories(AdminOnly, ListView):
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 5
    queryset = models.Category.objects.annotate(product_count=Count('product')).order_by('id')


class CategoryCreate(AdminOnly, CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'category-form.html'
    success_url = reverse_lazy('ad:categories')


class CategoryEdit(AdminOnly, UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'category-form.html'
    pk_url_kwarg = 'cat_id'
    context_object_name = 'category'
    success_url = reverse_lazy('ad:categories')


class CategoryDelete(AdminOnly, DeleteView):
    model = models.Category
    pk_url_kwarg = 'cat_id'
    success_url = reverse_lazy('ad:categories')

    def form_valid(self, form):
        if not self.object.product_set.exists():
            self.object.delete()
        return redirect(self.success_url)


class CategoryDetails(AdminOnly, DetailView):
    model = models.Category
    template_name = 'category.html'
    pk_url_kwarg = 'cat_id'
    context_object_name = 'category'


class ProductSave(AdminOnly):
    model = models.Product
    form_class = forms.ProductForm
    template_name = 'product-form.html'

    def form_valid(self, form):
        image = form.cleaned_data['image_url']
        if hasattr(image, 'content_type'):
            form.instance.image_url = make_watermarked_thumbnail(image)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad:category_details', args=[self.object.category_id])


class ProductCreate(ProductSave, CreateView):
    def get_initial(self):
        return {'category': self.kwargs['cat_id']}


class ProductEdit(ProductSave, UpdateView):
    pk_url_kwarg = 'prod_id'


class ProductDetails(AdminOnly, DetailView):
    model = models.Product
    template_name = 'product.html'
    pk_url_kwarg = 'prod_id'
    context_object_name = 'product'


class ProductDelete(AdminOnly, DeleteView):
    model = models.Product
    pk_url_kwarg = "prod_id"

    def get_success_url(self):
        return reverse("ad:category_details", args=[self.kwargs["cat_id"]])



class Orders(AdminOnly, ListView):
    template_name = "orders.html"
    context_object_name = "orders"
    queryset = models.Order.objects.select_related("user", "product").order_by("-id")
