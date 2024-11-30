from rest_framework import serializers

from cats.models import Cat, Mission, Target


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['name', 'country', 'notes', 'complete_state']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete_state', 'targets']

    def create(self, validated_data):
        print(validated_data)
        targets_data = validated_data.pop('targets')
        print(targets_data)
        print(validated_data)
        if not 1 <= len(targets_data) <= 3:
            raise serializers.ValidationError("A mission must have 1-3 targets")

        mission = Mission.objects.create(**validated_data)
        targets = [
            Target(
                mission=mission,
                **target_data
            )
            for target_data in targets_data
        ]
        Target.objects.bulk_create(targets)
        return mission

