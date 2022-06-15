from rest_framework import mixins, viewsets


class OnlyPostModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class OnlyMeModelViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    pass
