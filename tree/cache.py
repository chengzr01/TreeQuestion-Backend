from .models import *
from datetime import *
from django.http import JsonResponse


def refresh_cache(request):
    if request.method == "POST":
        for knowledge in Knowledge.objects.all():
            if knowledge.datetime + timedelta(days=7) < datetime.utcnow():
                knowledge.delete()
        for graph in Graph.objects.all():
            if graph.datetime + timedelta(days=7) < datetime.utcnow():
                graph.delete()
        for key in Key.objects.all():
            if key.datetime + timedelta(days=7) < datetime.utcnow():
                key.delete()
        for distractor in Distractor.objects.all():
            if distractor.datetime + timedelta(days=7) < datetime.utcnow():
                distractor.delete()
        for question in Question.objects.all():
            if question.datetime + timedelta(days=7) < datetime.utcnow():
                question.delete()
        return JsonResponse({
            'code': 200,
            'data': "Refresh cache succeeded!"
        },
                            status=200)


def delete_cache(request):
    if request.method == "POST":
        Knowledge.objects.all().delete()
        Graph.objects.all().delete()
        Key.objects.all().delete()
        Distractor.objects.all().delete()
        Question.objects.all().delete()
        return JsonResponse({
            'code': 200,
            'data': "Deleting cache succeeded!"
        },
                            status=200)