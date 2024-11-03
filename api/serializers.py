from rest_framework import serializers
from my_app.models import Messages, Room, Topics

class MessageSerilaizer(serializers.ModelSerializer):
  class Meta:
    model = Messages
    fields = '__all__'

class RoomSerilaizer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields = '__all__'

class TopicSerilaizer(serializers.ModelSerializer):
  class Meta:
    model = Topics
    fields = '__all__'
