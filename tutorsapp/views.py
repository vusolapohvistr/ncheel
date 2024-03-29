from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
import pymongo
import datetime
from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from .models import TestTemplates, TestSchedule, Answers, Images
from .serializers import TestTemplatesSerializer, TestScheduleSerializer, AnswersSerializer, ImageSerializer
import json
import secrets

# Create your views here.


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            django_login(request, user)
            return HttpResponse(request)
        else:
            return HttpResponse('Incorrect login or password', status=401)
    else:
        return HttpResponse(status=404)


def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        User.objects.create_user(data['username'], data['email'], data['password'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


class TestTemplatesView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = TestTemplates.objects.all()
    serializer_class = TestTemplatesSerializer

    def list(self, request, *args, **kwargs):
        response_data = [{'title': template.title,
                          'last_update_date': template.last_update_date,
                          'id': template.id,
                          'description': template.description}
                         for template in TestTemplates.objects.filter(id_user=request.user)]
        print(response_data)
        return Response(response_data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        template = TestTemplates.objects.get(pk=pk)
        if request.user != template.id_user:
            return Response(status=401)
        mc = pymongo.MongoClient('mongodb://localhost:27017/')['ncheel']
        print(template)
        response_data = {
            'title': template.title,
            'template': mc["test_templates"].find_one({'id': template.id})['test_template'],
            'last_update_date': template.last_update_date,
            'description': template.description
        }
        print(response_data)
        return Response(response_data)


class TestScheduleView(viewsets.ModelViewSet):
    queryset = TestSchedule.objects.all()
    serializer_class = TestScheduleSerializer


class AnswersView(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer

    def list(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, pk=None, *args, **kwargs):
        mc = pymongo.MongoClient('mongodb://localhost:27017')["ncheel"]
        answer = Answers.objects.get(pk=pk)
        answer.name, answer.surname, answer.class_name = \
            request.data['name'], request.data['surname'], request.data['class_name']
        answer.save()
        mc['answers'].insert_one({'id': answer.id, 'answer': request.data['answer']})
        return Response(status=200)


    @action(detail=True)
    def get_test_by_key(self, request):
        key = request.query_params['key']
        victim_mac_address = request.query_params['m']
        answer = Answers.objects.get(key=key)

        # check student's mac, if empty fill it, else 404
        if answer.victim_mac_address == 'empty':
            answer.victim_mac_address = victim_mac_address
        elif answer.victim_mac_address != victim_mac_address:
            return Response(status=404)
        else:
            answer.victim_mac_address = victim_mac_address
        # check time
        if answer.id_schedule.time_start > datetime.datetime.now() \
                or answer.id_schedule.time_end < datetime.datetime.now():
            return Response(status=404)

        mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
        return Response({
            'template': mongo_client["ncheel"]  # LOOK 1 LINE DOWN !!!
            ["test_templates"].find_one({'id': answer.id_schedule.id_test_template})['template'],
            'time_start': answer.id_schedule.time_start,
            'time_end': answer.id_schedule.time_end,
            'answer_id': answer.id
        })


class ImageView(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    def list(self, request, *args, **kwargs):
        query = request.query_params
        print(query)
        if query:
            try:
                image = Images.objects.get(key=query['key'])
                return Response(image.image.path)
            except Exception:
                return Response(status=404)
        else:
            return Response([{'path': image.image.url} for image in Images.objects.all()])

    def retrieve(self, request, *args, **kwargs):
        return Response(status=404)



def main(request):
    print(request)
    return render(request, 'tutorsapp/login/index.html')


def test_page(request):
    key = request.GET['key']
    answer = Answers.objects.get(key=key)
    if not answer:
        return HttpResponse(status=404)
    if answer.id_schedule.time_start > datetime.datetime.now() \
            or answer.id_schedule.time_end < datetime.datetime.now():
        return HttpResponseRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    render_to_response('tutorsapp/test_page.html')



