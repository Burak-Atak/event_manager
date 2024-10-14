from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()

    @action(detail=True, methods=['get'])
    def detailed(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='detailed')
    def detailed_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MultiAuthViewSetMixin(object):
    def get_permissions(self):
        try:
            if self.action in self.authenticated_user_actions:
                return [IsAuthenticated()]
            elif self.action in self.anonymous_user_actions:
                return []
            else:
                return super(MultiAuthViewSetMixin, self).get_permissions()


        except (KeyError, AttributeError):
            return super(MultiAuthViewSetMixin, self).get_permissions()
