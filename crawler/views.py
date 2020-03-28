from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy

from .form import WantedItemCreateForm

from blog.views import ListViewPaginator

from .models import *

import requests
import json

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

    paginate_by = 20

class WantedItemCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'crawler.add_wanteditem'
    model = WantedItem
    template_name = 'crawler/create.html'
    success_url = reverse_lazy('crawler:create')
    form_class = WantedItemCreateForm

class WantedItemDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'crawler.delete_wanteditem'
    model = WantedItem
    success_url = reverse_lazy('crawler:index')