from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import New, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = New
    template_name = 'news/home_news.html'
    context_object_name = 'news'
    queryset = New.objects.select_related('category')
    mixin_prop = 'Hello world'
    paginate_by = 5

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # def get_queryset(self):
    # return New.objects.filter(is_published=True).select_related('category')
    # жадная загрузка


# def index(request):
#     news = New.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)

# send to mail
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'duk1e@urk.net', ['duk1e.drum@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class NewsByCategory(MyMixin, ListView):
    model = New
    template_name = 'news/home_news.html'
    context_object_name = 'news'
    allow_empty = False  # не показывать если нет новости или путстого списка
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return New.objects.filter(category_id=self.kwargs['category_id']).select_related('category')


# def get_category(request, category_id):
#     news = New.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


class ViewNews(DetailView):
    model = New
    context_object_name = 'news_item'

    # pk_url_kwarg = 'news_id'
    # template_name = 'news/new_detail.html'


# def view_news(request, news_id):
#     news_item = get_object_or_404(New, pk=news_id)
#     # try:
#     #     news_item = New.objects.get(pk=news_id)
#     # except:
#     #     print('Bygagasheka!')
#     #     return Http404('My model')
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# not connected with model
# ----------------------------
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # ** - распаковка словаря
#             news = New.objects.create(**form.cleaned_data)
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # raise_exception = True
    # success_url = reverse_lazy('home')


# Connected with model
# -----------------------------------
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

# class based views


# pagination

def test(request):
    objects = ['john', 'paul', 'goerge', 'michael', 'paul', 'mike', 'john2', 'paul2', 'goerge2', 'michael2', 'paul2',
               'mike2', 'john3', 'paul3', 'goerge3', 'michael3', 'paul3', 'mike3']
    paginator = Paginator(objects, 3)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})
