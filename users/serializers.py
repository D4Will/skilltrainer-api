from rest_framework import serializers
from users.models import User

class RegularUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = [
      'username',
      'email',
      'password',
    ]
  
  def create(self, validated_data):
    user = User(
      username=validated_data['username'],
      email=validated_data['email']
    )
    # Uses the User model method to set the password to its hashed value rather than plaintext
    user.set_password(validated_data['password'])
    user.save()
    return user

  def validate(self, data):
    if User.objects.filter(email=data['email']).exists():
      raise serializers.ValidationError('Email must be unique.')
    if len(data['password']) < 8:
      raise serializers.ValidationError('Password must be at least 8 characters.')
    return data