from rest_framework import mixins, viewsets


class OnlyPostModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass
