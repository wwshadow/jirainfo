from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import TbJirauser

class TbjirauserSerializer(Serializer):
    id = serializers.IntegerField(label="主键", read_only=True,
                                  error_messages={"required": "read_only为真，表示此字段只在序列化时做检查，反序列化不做检查"})
    jiraemail = serializers.CharField(required=False)
    jiraid = serializers.UUIDField(required=False)
    jirakey = serializers.CharField()
    jiraname = serializers.CharField(required=False)
    sessiontoken = serializers.CharField(required=False)
    jiratotptoken = serializers.CharField(required=False)
    tempotoken = serializers.CharField(required=False)
    projectname = serializers.CharField(required=False)
    groups = serializers.CharField(required=False)
    def create(self, validated_data):
        return TbJirauser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.jiraemail = validated_data.get('jiraemail', instance.jiraemail)
        instance.jiraid = validated_data.get('jiraid', instance.jiraid)
        instance.jirakey = validated_data.get('jirakey', instance.jirakey)
        instance.jiraname = validated_data.get('jiraname', instance.jiraname)
        instance.sessiontoken = validated_data.get('sessiontoken', instance.sessiontoken)
        instance.jiratotptoken = validated_data.get('jiratotptoken', instance.jiratotptoken)
        instance.tempotoken = validated_data.get('tempotoken', instance.tempotoken)
        instance.projectname = validated_data.get('projectname', instance.projectname)
        instance.groups = validated_data.get('groups', instance.groups)
        instance.save()
        return instance