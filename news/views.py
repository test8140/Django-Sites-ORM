from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import News, Category
from .forms import NewsForm
from .utils import MyMixin




def test(request):
    objects = ['kelli1', 'sara2', 'billi3', 'gari4', 'djon5', 'maikl6', 'genri7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})
 

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная'}
    # queryset = News.objects.select_related('category')
    mixin_prop = 'Hello World'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], 
                            is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    # login_url = '/admin/' # reverse_lazy('home')
    raise_exception = True


# def index(request):
    #news = News.objects.all()
    #context = {
        #'news': news,
        #'title': 'Список новостей',
    #}
    #return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
    # news = News.objects.filter(category_id=category_id)
    # category = Category.objects.get(pk=category_id)
    # context = {
        # 'news': news,
        # 'category': category,
    #}
    #return render(request, 'news/category.html', context)

# def view_views(request, news_id):
    # news_item = get_object_or_404(News, pk=news_id)
    # return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
    # if request.method == 'POST':
       # form = NewsForm(request.POST)
        # if form.is_valid():
            # news = form.save()
            # return redirect(news)
    # else:
        # form = NewsForm()
    # return render(request, 'news/add_news.html', {'form': form})

    


