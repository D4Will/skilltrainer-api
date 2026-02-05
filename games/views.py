from rest_framework import generics, status
from rest_framework.views import APIView
from games.models import TargetScore
from games.serializers import TargetScoreSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
    

class TargetScoreListCreateView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    target_scores = TargetScore.objects.filter(user=request.user)
    serializer = TargetScoreSerializer(target_scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

  def post(self, request):
    target_data = request.data
    target_data['user'] = request.user.id

    serializer = TargetScoreSerializer(data=target_data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class TargetScoreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAuthenticated]
  queryset = TargetScore.objects.all()
  serializer_class = TargetScoreSerializer
  lookup_url_kwarg = 'score_id'

  