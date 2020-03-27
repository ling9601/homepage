from django.shortcuts import render, HttpResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

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