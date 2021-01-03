from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.contrib import messages

import random
import re
import markdown2

from . import util


class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html",{
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
                search = form.cleaned_data["search"]
                if util.get_entry(search) == None:
                    list = util.list_entries()
                    res = [ x for x in list if re.search(search.capitalize(), x)]
                    return render(request,"encyclopedia/results.html",{
                    "search":search.capitalize(),
                    "entries":res
                    })
                else:
                    return render(request, "encyclopedia/display.html",{
                    "entries":util.get_entry(search),
                    "name":search
            })

def entry(request, name):
        return render(request, "encyclopedia/display.html",{
        "entries": markdown2.markdown(util.get_entry(name)),
        "name":name
    })
def newpage(request):
    list = util.list_entries()
    return render(request, "encyclopedia/newpage.html",{"list":list})

def savenewpage(request):
    list = util.list_entries()
    title = request.POST.get("title")
    markdowncontent = request.POST.get("markdowncontent")
    if util.get_entry(title) == None:
        save = util.save_entry(title,markdowncontent)
        return render(request,"encyclopedia/savecontent.html",{"title":title, "markdowncontent":markdowncontent})
    else:
        messages.success(request, 'Title already exist. Please enter a new title and its markdown content.')
        return HttpResponseRedirect(reverse("encyclopedia:newpage"))

def randompage(request):
    list = util.list_entries()
    n = random.randint(0,4)
    search = markdown2.markdown(util.get_entry(list[n]))
    return render(request, "encyclopedia/randompage.html",{"list":search})

def edit(request):
    list = util.list_entries()
    return render(request, "encyclopedia/edit.html")
