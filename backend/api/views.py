from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer
from products.models import Product


@api_view(["GET", "POST"])
def api_home(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, 
            many=True, 
            context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(
            data=request.data, 
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    