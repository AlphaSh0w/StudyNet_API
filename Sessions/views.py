from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Session
from .serializers import SessionSerializer
from Accounts.models import User
# Create your views here.

class SessionList(APIView):
    """
    Retrieves the list of sessions.
    Can be filtered by section.
    """

    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            return Session.objects.filter(assignment__teacher_section__section__code=section)
        else:
            return Session.objects.all()
    
    def get(self,request):
        sessions = self.get_queryset()
        seriliazer = SessionSerializer(sessions, many=True)
        return Response(seriliazer.data)
    
    def post(self, request):
        if request.user.user_type == User.Types.TEACHER:
            serializer = SessionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"Unauthorized":"Only teachers may create sessions."},status=status.HTTP_401_UNAUTHORIZED)
