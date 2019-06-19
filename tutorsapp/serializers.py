from rest_framework import serializers
from .models import TestTemplates, TestSchedule, Answers, Images
from django.contrib.auth.models import User
import pymongo
import json
import secrets
from django.core.mail import send_mass_mail


class TestTemplatesSerializer(serializers.ModelSerializer):
    test_template_json = serializers.CharField(write_only=True)
    id_user = serializers.CharField(read_only=True)

    class Meta:
        model = TestTemplates
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        test_template = TestTemplates(
            id_user=user,
            title=validated_data['title'],
            max_possible_result=validated_data['max_possible_result'],
            description=validated_data['description']
        )
        test_template.save()
        mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
        db = mongo_client["ncheel"]
        col = db["test_templates"]
        col.insert_one({'test_template': json.loads(validated_data['test_template_json']),
                        'id': test_template.id})
        return test_template


# DON'T FORGET TO MAKE LINK GENERATOR
class TestScheduleSerializer(serializers.ModelSerializer):
    emails = serializers.CharField(write_only=True)

    class Meta:
        model = TestSchedule
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        test = TestSchedule.objects.create(id_test_template=validated_data['id_test_template'],
                                           time_start=validated_data['time_start'],
                                           time_end=validated_data['time_end'])
        sends = []
        subject = test.id_test_template.title
        from_email = ''  # DON'T FORGET FILL THIS IF NOT G'MAIL
        for email in validated_data['emails'].split(','):
            key = secrets.token_urlsafe(32)
            Answers.objects.create(email=email,
                                   key=key,
                                   id_schedule=test.id)
            message = ''  # DON'T FORGET TO GENERATE LINK IN MESSAGE
            # to (your www address) + 'test?key=' + key
            sends.append((subject, message, from_email, [email]))
        send_mass_mail(tuple(sends))


class AnswersSerializer(serializers.ModelSerializer):
    test_answers_json = serializers.CharField(write_only=True)

    class Meta:
        model = Answers
        fields = ('date_pass', 'name', 'surname', 'class_name', 'id', 'victim_mac_address')

    def update(self, instance, validated_data):
        print(validated_data)
        mongo_client = pymongo.MongoClient('mongodb://localhost:27017')["ncheel"]
        answer = Answers.objects.get(id)
        # end it, student's answer sheet
        pass


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'




