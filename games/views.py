from rest_framework import status
from rest_framework.views import APIView
from datetime import timedelta
from games.models import TargetScore, ReactionScore, TypingScore
from games.serializers import TargetScoreSerializer, ReactionScoreSerializer, TypingScoreSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response    

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

    if len(target_scores) == 0:
      return Response(status=status.HTTP_404_NOT_FOUND)

    average_time = 0
    for score in target_scores:
      average_time += (score.time_elapsed / timedelta(milliseconds=1)) / score.targets
    average_time = round(average_time / len(target_scores), None)

    average_accuracy = 0
    for score in target_scores:
      average_accuracy += score.targets/score.clicks * 100
    average_accuracy = round(average_accuracy / len(target_scores), 1)
    
    # serializer = TargetScoreSerializer(target_scores, many=True)
    return Response({'average_time': average_time, 'average_accuracy': average_accuracy}, status=status.HTTP_200_OK)
    

class ReactionScoreListCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    reaction_scores = ReactionScore.objects.filter(user=request.user)
    reaction_scores = reaction_scores.order_by('-id')[:10]
    serializer = ReactionScoreSerializer(reaction_scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    reaction_data = request.data
    reaction_data['user'] = request.user.id

    serializer = ReactionScoreSerializer(data=reaction_data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class ReactionScoreAggregateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    aggregate_amount = request.data['score_amount']
    reaction_scores = ReactionScore.objects.filter(user=request.user)
    reaction_scores = reaction_scores.order_by('-id')[:aggregate_amount]

    if len(reaction_scores) == 0:
      return Response(status=status.HTTP_404_NOT_FOUND)

    average_time = 0
    for score in reaction_scores:
      sub_avg = 0
      for time in score.reaction_times:
        sub_avg += time
      sub_avg = round(sub_avg / len(score.reaction_times))
      average_time += sub_avg
    
    average_time = round(average_time / len(reaction_scores))

    return Response({'average_time': average_time}, status=status.HTTP_200_OK)

  

class TypingScoreListCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    typing_scores = TypingScore.objects.filter(user=request.user)
    typing_scores = typing_scores.order_by('-id')[:10]
    serializer = TypingScoreSerializer(typing_scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    typing_data = request.data
    typing_data['user'] = request.user.id

    serializer = TypingScoreSerializer(data=typing_data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class TypingScoreAggregateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request): 
    aggregate_amount = request.data['score_amount']
    typing_scores = TypingScore.objects.filter(user=request.user)
    typing_scores = typing_scores.order_by('-id')[:aggregate_amount]

    if len(typing_scores) == 0:
      return Response(status=status.HTTP_404_NOT_FOUND)

    average_wpm = 0
    average_accuracy = 0
    average_raw = 0
    for score in typing_scores:
      average_wpm += score.wpm
      average_accuracy += score.accuracy
      average_raw += score.raw_wpm

    average_wpm = round(average_wpm / len(typing_scores))
    average_accuracy = round(average_accuracy / len(typing_scores), 1)
    average_raw = round(average_raw / len(typing_scores))

    return Response({
      'average_wpm': average_wpm, 
      'average_accuracy': average_accuracy,
      'average_raw_wpm': average_raw
      }, status=status.HTTP_200_OK)