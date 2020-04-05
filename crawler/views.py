from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy


from .form import *

from blog.views import ListViewPaginator

from .models import *

import requests
import json
import datetime
from django_pandas.io import read_frame
import pytz

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def status(request):
    resp = requests.get('http://localhost:6800/listjobs.json?project=app')
    json_pretty = json.dumps(resp.json(), indent=4)
    return HttpResponse(json_pretty, content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def get_log(request, id):
    resp = requests.get('http://localhost:6800/logs/app/store/{}.log'.format(id))
    return HttpResponse(resp, content_type='text/plain')


class WantedItemIndexVIew(PermissionRequiredMixin,ListViewPaginator):
    permission_required = 'crawler.view_wanteditem'
    model = WantedItem
    template_name = 'crawler/index.html'
    context_object_name = 'wanted_item_list'
    paginate_by = 50

    def get_queryset(self):
        return super(WantedItemIndexVIew, self).get_queryset().filter(
            created_by = self.request.user,
        )

class WantedItemCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'crawler.add_wanteditem'
    model = WantedItem
    success_url = reverse_lazy('crawler:create')
    form_class = WantedItemForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WantedItemUpdateView(PermissionRequiredMixin,UserPassesTestMixin,UpdateView):
    permission_required = 'crawler.change_wanteditem'
    model = WantedItem
    success_url = reverse_lazy('crawler:index')
    form_class = WantedItemForm

    def test_func(self):
        return self.get_object().created_by == self.request.user
    
class WantedItemDeleteView(PermissionRequiredMixin,UserPassesTestMixin,DeleteView):
    permission_required = 'crawler.delete_wanteditem'
    model = WantedItem
    success_url = reverse_lazy('crawler:index')

    def test_func(self):
        return self.get_object().created_by == self.request.user

class BaseItemDetailView(PermissionRequiredMixin,DeleteView):
    model = BaseItem_dj
    permission_required = 'crawler.view_baseitem_dj'

    def get_template_names(self):
        if 'modal' in self.kwargs:
            return ['crawler/baseitem_dj_modal.html']
        else:
            return ['crawler/baseitem_dj_detail.html']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))

        query = StoreItem_dj.objects.filter(
            base_item = self.object,
            scrapy_item__start_time__lte = now,
            scrapy_item__start_time__gt = now-datetime.timedelta(days=30),
        )
        if not query:
            context['data'] = None
            return context
        f = read_frame(query)
        f = f[['price','num','scrapy_item']]
        max = f.groupby('scrapy_item').max()['price']
        min = f.groupby('scrapy_item').min()['price']
        f['price_total'] = f['price'] * f['num']
        mean = f.drop(['price'],axis=1).groupby(['scrapy_item']).sum()
        mean = mean['price_total']/mean['num']
        
        context['data'] = zip(max.index.values, max.values, mean.values, min.values)

        return context

def search(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id.isdigit() and BaseItem_dj.objects.filter(pk=int(id)):
            return HttpResponseRedirect(reverse_lazy('crawler:detail',kwargs={'pk':int(id)}))
        else:
            return render(request, 'crawler/error.html', context={'error_message':'ID不存在'})