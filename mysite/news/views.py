from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import New, Category
from .forms import NewsForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeNews(MyMixin, ListView):
    model = New
    template_name = 'news/home_news.html'
    context_object_name = 'news'
    queryset = New.objects.select_related('category')
    mixin_prop = 'Hello world'

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


def test(request):
    return HttpResponse('<h2>Test page!</h2>')


class NewsByCategory(MyMixin, ListView):
    model = New
    template_name = 'news/home_news.html'
    context_object_name = 'news'
    allow_empty = False  # не показывать если нет новости или путстого списка

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
