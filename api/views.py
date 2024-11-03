from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_app.models import Messages, Room, Topics
from .serializers import MessageSerilaizer, RoomSerilaizer, TopicSerilaizer


@api_view(['GET'])
def all_view(request):
  message = Messages.objects.all()
  room = Room.objects.all()
  topic = Topics.objects.all()
  
  message_serializer = MessageSerilaizer(message, many=True)
  room_serializer = RoomSerilaizer(room, many=True)
  topic_serializer = TopicSerilaizer(topic, many=True)
  
  serializer = {
    'messages':message_serializer.data, 
    'rooms': room_serializer.data,
    'topics':topic_serializer.data
  }
  
  return Response(serializer)

