from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cats.models import Cat, Mission, Target
from cats.serializers import CatSerializer, MissionSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # For PATCH requests, only update salary
        if kwargs.get('partial', False):
            serializer = self.get_serializer(instance, data={'salary': request.data.get('salary', instance.salary)},
                                             partial=True)
        else:
            serializer = self.get_serializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response(
                {"error": "Cannot delete mission assigned to a cat"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat_id')

        try:
            cat = Cat.objects.get(id=cat_id)
        except Cat.DoesNotExist:
            return Response(
                {"error": "Cat not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        mission.cat = cat
        mission.save()
        return Response(MissionSerializer(mission).data)

    @action(detail=True, methods=['patch'])
    def update_target(self, request, pk=None):
        mission = self.get_object()
        target_id = request.data.get('target_id')
        notes = request.data.get('notes')
        complete_state = request.data.get('complete_state')

        try:
            target = Target.objects.get(id=target_id, mission=mission)
        except Target.DoesNotExist:
            return Response(
                {"error": "Target not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if mission.complete_state or target.complete_state:
            return Response(
                {"error": "Cannot update completed target/mission"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if notes is not None and target.complete_state is False:
            target.notes = notes
        if complete_state:
            target.complete_state = complete_state
        target.save()

        # Check if all targets are complete
        if all(t.complete_state for t in mission.targets.all()):
            mission.complete_state = True
            mission.save()

        return Response(MissionSerializer(mission).data)
