from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse
import random
import markdown2
from . import util

def convert_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdown2.markdown(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, topic):

        if util.get_entry(topic) == None:
            return render(request, "encyclopedia/apology.html", {
                 "message":'No results found'
            })
        else:
            return render(request, "encyclopedia/content.html", {
                "title": topic,
                "content": convert_to_html(topic)
            })

def search(request):
     topic = request.POST['q']

     if convert_to_html(topic) is not None:
          return render(request, 'encyclopedia/content.html', {
               "title": topic,
               "content": convert_to_html(topic)
          })

     elif convert_to_html(topic) is None:

        entries = util.list_entries()
        recommend = []

        for entry in entries:
             if topic.lower() in entry.lower():
                  recommend.append(entry)

        if len(recommend) == 0:
             return render(request, "encyclopedia/apology.html", {
                  "message":'No page found'
             })

        return render(request, "encyclopedia/search.html", {
             "topic": topic,
             "recommend": recommend
        })

def create(request):
     if request.method == 'GET':
          return render(request, "encyclopedia/create_page.html")

     if request.method == 'POST':
          title = request.POST['head']
          content = request.POST['content']

          if convert_to_html(title) is None:
               util.save_entry(title, content)

               return render(request, "encyclopedia/content.html", {
                    "title":title,
                    "content":convert_to_html(title)
               })
          else:
               return render(request, 'encyclopedia/apology.html', {
                    'message':'Topic already exist!'
               })

def edit(request):
     if request.method == 'POST':
          topic = request.POST['title_of_topic']
          return render(request, "encyclopedia/edit.html", {
               "topic":topic,
               "content":util.get_entry(topic)
          })

     else:
          return redirect("/")

def save(request):
     if request.method == 'POST':
          topic = request.POST['head']
          content = request.POST['content']

          util.save_entry(topic, content)

          return render(request, "encyclopedia/content.html", {
               "title":topic,
               "content":convert_to_html(topic)
          })

     if request.method == 'GET':
          return redirect("/")

def random_topic(request):
     entries = util.list_entries()

     random_ = random.choice(entries)

     return render(request, "encyclopedia/content.html", {
          "title":random_,
          "content":convert_to_html(random_)
     })
