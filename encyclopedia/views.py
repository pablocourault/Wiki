
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from random import randrange

from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", 
                  {"entries": util.list_entries()})


def wiki(request, name):

    if util.get_entry(name) == None:

        return render(request, 
                    "encyclopedia/error.html",
                    {"mensaje": "the page you are trying to access does not exist."})

    else:

        markdowner = Markdown()

        return render(request, 
                    "encyclopedia/wiki.html",
                    {"titulo": name, "contenido":markdowner.convert(util.get_entry(name))})


def edit(request, name):

    class wikimodify(forms.Form):
            description = forms.CharField( widget=forms.Textarea,
                                           required="True",
                                           label=False,
                                           initial=util.get_entry(name))


    if request.method == "GET":

        formulario = wikimodify()

        return render(request, "encyclopedia/edit.html", {
                  "titulo": name, 
                  "formulario": wikimodify()})
    

    if request.method == "POST":

        formulario = wikimodify(request.POST)

        if formulario.is_valid():
            
            description = formulario.cleaned_data["description"]

            util.save_entry(name, description)

        return HttpResponseRedirect(reverse("wiki", args=[name]))


def create(request):

    class wikicreate(forms.Form):
            title = forms.CharField(widget=forms.TextInput,required="True")
            description = forms.CharField( widget=forms.Textarea,
                                           required="True")
    
    if request.method == "GET":

        return render(request, "encyclopedia/create.html", {"formulario": wikicreate()})

    if request.method == "POST":

        formulario = wikicreate(request.POST)

        if formulario.is_valid():

            title = formulario.cleaned_data["title"]

            description = formulario.cleaned_data["description"]

            if util.get_entry(title) == None:

                util.save_entry(title, description)
                return HttpResponseRedirect(reverse("wiki", args=[title]))

            else:

                return render(request, 
                    "encyclopedia/error.html",
                    {"mensaje": "the page you are trying to add already exists."})


def random(request):

    lista = util.list_entries()

    aleatorio = randrange(0,len(util.list_entries()))

    random_title = lista[aleatorio]

    markdowner = Markdown()
    
    return render(request, 
                  "encyclopedia/wiki.html",
                  {"titulo": random_title, 
                   "contenido":markdowner.convert(util.get_entry(random_title))})


def search(request):

    if request.method == "POST":

        consulta = request.POST.get("q")

        entries = util.list_entries()

        if consulta in entries:

            markdowner = Markdown()

            return render(request, 
                    "encyclopedia/wiki.html",
                    {"titulo": consulta, "contenido":markdowner.convert(util.get_entry(consulta))})

        else: 
            
            matches = []

            for entry in entries:

                if consulta.upper() in entry.upper():
                    matches.append(entry)
            
            if len(matches) > 0:

                 return render(request, "encyclopedia/index.html", 
                               {"entries": matches})

            else:

                return render(request, 
                    "encyclopedia/error.html",
                    {"mensaje": "no matches found for your search"})


