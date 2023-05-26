from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CarBrand
from .serializers import CarBrandSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission



# class MyProtectedView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         # Обработка запроса
#         return Response(...)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CanEditCarBrandPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_edit_permission()

class CarBrandView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarBrandDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CanEditCarBrandPermission]
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    lookup_field = 'id'
