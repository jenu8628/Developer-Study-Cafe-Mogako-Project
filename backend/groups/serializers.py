from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Group, Study, Apply


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_members(self, group):
        return [ single_member.apply_user.id for single_member in Apply.objects.filter(study=group.study) ]


class StudySerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = '__all__'
    def get_members(self, study):
        return [ single_member.apply_user.id for single_member in Apply.objects.filter(study=study) ]


class ApplySerialier(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = ('id', 'apply_user')

