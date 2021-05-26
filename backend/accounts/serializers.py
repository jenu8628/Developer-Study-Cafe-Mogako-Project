from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Profile
from groups.models import Apply

User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class ProfileLiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'message']

class ProfileSerializer(serializers.ModelSerializer):
    study = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(use_url=True, required=False)
    img_url = serializers.URLField(read_only=True)
    money = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

    def get_study(self, profile):
        from groups.serializers import StudySerializer
        
        user = User.objects.get(id=profile.user.id)
        applied_study = Apply.objects.filter(apply_user=user)
        study_list = [ i.study for i in applied_study]
        study_data = [ StudySerializer(i).data for i in study_list]

        return study_data
        
    def get_username(self, profile):
        target_user = User.objects.get(id=profile.user.id)
        return target_user.username

    def get_email(self, profile):
        target_user = User.objects.get(id=profile.user.id)
        return target_user.email
    
    def get_money(self, profile):
        target_user = User.objects.get(id=profile.user.id)
        return target_user.money