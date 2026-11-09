from django.shortcuts import render
from api.mixins import StaffEditorPermissionsMixin, UserQuerySetMixin

from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductListCreateAPIView(UserQuerySetMixin, StaffEditorPermissionsMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    user_field = 'user'
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)

class ProductDetailAPIView(StaffEditorPermissionsMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

class ProductUpdateAPIView(StaffEditorPermissionsMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(StaffEditorPermissionsMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    
    def perform_destroy(self, instance):
        #super().perform_destroy(instance)
        instance.delete()

class ProductMixinView(StaffEditorPermissionsMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)

# @api_view
# def product_alt_view(request, *args, **kwargs):
#     if method == "GET":
#         if pk is not None:
#             obj = get_object_or_404(Product, pk=pk)
#             data = ProductSerializer(obj, many=False).data
#             return Response(data)
#         queryset = Product.objects.all()
#         data = ProductSerializer(queryset, many=False).data
#         return Response(data)
    
#     if method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)