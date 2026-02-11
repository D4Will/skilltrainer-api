from rest_framework import status
from rest_framework.views import APIView
from datetime import timedelta
from games.models import TargetScore
from games.serializers import TargetScoreSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Sum
    

class TargetScoreListCreateView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    target_scores = TargetScore.objects.filter(user=request.user)
    target_scores = target_scores.order_by('-id')[:10]
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
  
class TargetScoreAggregateView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    aggregate_amount = request.data['score_amount']
    target_scores = TargetScore.objects.filter(user=request.user)
    target_scores = target_scores.order_by('-id')[:aggregate_amount]

    average_time = 0
    for score in target_scores:
      average_time += (score.time_elapsed / timedelta(milliseconds=1)) / score.targets
    average_time = average_time / len(target_scores)

    average_accuracy = 0
    for score in target_scores:
      average_accuracy += score.targets/score.clicks * 100
    average_accuracy = average_accuracy / len(target_scores)
    
    # serializer = TargetScoreSerializer(target_scores, many=True)
    return Response({'average_time': average_time, 'average_accuracy': average_accuracy}, status=status.HTTP_200_OK)
    
