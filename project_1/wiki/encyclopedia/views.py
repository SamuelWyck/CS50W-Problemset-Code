from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
import random

markdown = Markdown()

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry=None):

    page = util.get_entry(entry)
    if page == None:
        return render(request, "encyclopedia/error.html", {
            "error_message": f"Page for '{entry.capitalize()}' not found."
        })
    
    page = markdown.convert(page)
    return render(request, "encyclopedia/entry.html", {
        "entry": page, "title": entry.capitalize()
    })


def results(request):

    q = request.GET["q"]
    if not q:
        return HttpResponseRedirect(reverse("index"))
    
    entry = util.get_entry(q)

    if entry == None:
        results = []
        entries = util.list_entries()
        for item in entries:
            match = re.search(q, item, re.IGNORECASE)
            if match:
                results.append(item)
        
        return render(request, "encyclopedia/results.html", {
            "results": results
        })
    
    entry = markdown.convert(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, "title": q.capitalize()
    })
    

def new_page(request):
    
    if request.method == "POST":
        title = request.POST["title"].strip()
        content = request.POST["content"]
        if not title or not content:
            return render(request, "encyclopedia/error.html", {
            "error_message": "All fields must be filled to create a new page."})
        
        check = util.get_entry(title)
        if check != None:
            return render(request, "encyclopedia/error.html", {
            "error_message": f"A page with the title: '{title}' already exists."})

        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry_page", args=[title]))
    
    return render(request, "encyclopedia/new_page.html")


def edit_page(request, entry):

    if request.method == "POST":
        if not request.POST["content"]:
            return render(request, "encyclopedia/error.html", {
            "error_message": "Page content cannot be empty."})
    
        content = request.POST["content"]
        util.save_entry(entry, content)
        return HttpResponseRedirect(reverse("entry_page", args=[entry]))

    content = util.get_entry(entry)

    return render(request, "encyclopedia/edit_page.html", {
        "content": content, "title": entry})


def get_random_page(requests):
    
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entry_page", args=[entry]))
