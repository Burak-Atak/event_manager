from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from core.views import MultiSerializerViewSetMixin, MultiAuthViewSetMixin
from users.filters import UserFilter
from users.models import User
from users.serializers import UserDetailedSerializer, UserSerializer, UserRegistrationSerializer, UserLoginSerializer, \
    UserLoginResponseSerializer
from users.service import UserService


class UserViewSet(MultiSerializerViewSetMixin, MultiAuthViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    service = UserService()
    serializer_class = UserDetailedSerializer
    serializer_action_classes = {
        'profile': UserDetailedSerializer,
        'detailed': UserDetailedSerializer,
        'register': UserRegistrationSerializer,
        'register_admin': UserRegistrationSerializer,
        'login': UserLoginSerializer,
        'list': UserSerializer,
    }
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    permission_classes = [IsAdminUser]
    authenticated_user_actions = ['profile', 'update', 'partial_update']
    anonymous_user_actions = ['register', 'login']
    ordering_fields = ("date_joined", "modified_date")
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ['retrieve', 'list']:
            without_settings = User.objects.without_settings()
            return without_settings

        return queryset

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        self.service.update_user(self.request.user, serializer.validated_data)

    @action(detail=False, methods=['get'])
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.service.register_user(serializer.validated_data)
        response = UserDetailedSerializer(user).data
        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = self.service.login_user(serializer.validated_data)
        response = UserLoginResponseSerializer(response_data).data

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[])
    def register_admin(self, request):
        # This is for API testing purpose only
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.service.register_user(serializer.validated_data, is_admin=True)
        response = UserDetailedSerializer(user).data
        return Response(response, status=status.HTTP_201_CREATED)
