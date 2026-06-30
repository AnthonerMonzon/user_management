from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsSuperAdmin, IsSuperAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model with role-based access control.
    - SuperAdmin: Full CRUD access to all users
    - Editor: Read-only access to all users
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Custom permission handling:
        - Only SuperAdmin can create/update/delete users
        - All authenticated users can list/retrieve users
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSuperAdmin]
        else:
            permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def editors(self, request):
        """Get all Editor users"""
        if not request.user.is_superadmin():
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        editors = User.objects.filter(user_type=User.UserType.EDITOR)
        serializer = UserSerializer(editors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def superadmins(self, request):
        """Get all SuperAdmin users"""
        if not request.user.is_superadmin():
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        superadmins = User.objects.filter(user_type=User.UserType.SUPERADMIN)
        serializer = UserSerializer(superadmins, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Login view for obtaining authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return Response(
                {'error': f'Authentication error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
