from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django import forms 
from . import util
import markdown2
import random2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query=request.POST.get('q')
    result=set()
    actual_entry=util.list_entries()
    lower_case_entry=list(map(lambda x: x.lower(),actual_entry))
    if query.lower() in lower_case_entry:
        return HttpResponseRedirect(reverse('detail',args=(actual_entry[lower_case_entry.index(query.lower())],)))
    else:
        for i in lower_case_entry:
            if query.lower() in i:
                result.add(actual_entry[lower_case_entry.index(i)])
        return render(request,'encyclopedia/search.html',{'result':result})
    

class CreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '50'}))
    md = forms.CharField(widget=forms.Textarea(attrs={'rows':2,'cols':5,'style': 'height: 300px; width:400px;'}), label='MarkDown Content')

def create(request):
    form=CreateForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            if util.get_entry(request.POST['title'])==None:
                title=request.POST.get('title')
                util.save_entry(request.POST['title'],request.POST['md'])
                return HttpResponseRedirect(reverse('detail',args=(title,)))
            else:
                return render(request,'encyclopedia/error.html')
    return render(request,'encyclopedia/create.html',{'form':form})

class EditForm(forms.Form):
    md = forms.CharField(widget=forms.Textarea(attrs={'rows':2,'cols':5,'style': 'height: 300px; width:400px;'}), label='MarkDown Content')

def edit(request,title):
    md=util.get_entry(title)
    form=EditForm(initial={'md':md})
    if request.method=="POST":
        util.save_entry(title,request.POST['md'])
        return HttpResponseRedirect(reverse('detail',args=(title,)))
    return render(request,'encyclopedia/edit.html',{'form':form,'title':title})


def detail(request,title):
    if util.get_entry(title)==None:
        return  render(request,'encyclopedia/not_found.html')
    entry_detail=markdown2.markdown(util.get_entry(title))
    context={
        'entry_title':title,
        'entry_detail':entry_detail
        }
    return render(request,'encyclopedia/detail.html',context)

def random(request):
    random_title=random2.choice(util.list_entries())
    entry_detail=markdown2.markdown(util.get_entry(random_title))
    context={
        'entry_title':random_title,
        'entry_detail':entry_detail
        }
    return render(request,'encyclopedia/detail.html',context)

