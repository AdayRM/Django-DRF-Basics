from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from market_app.models import Market, Product, Seller
from .serializers import MarketHyperlinkedSerializer, MarketSerializer, ProductHyperlinkedSerializer, ProductSerializer, SellerSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def markets_view(request):

    if request.method == "GET":
        markets = Market.objects.all()
        serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request': request})

        return Response(serializer.data)
    if request.method == "POST":
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def single_market_view(request, pk):

    if request.method == 'GET':
        market = get_object_or_404(Market, pk=pk)
        serializer = MarketSerializer(market, context={'request': request})
        return Response(serializer.data)
    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        market.delete()
        return Response("Market successfully deleted")
    if request.method == 'PUT':
        market = get_object_or_404(Market, pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'POST'])
def sellers_view(request):

    if request.method == "GET":
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == "POST":
        serializer = SellerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def single_seller_view(request, pk):
    if request.method == "GET":
        seller = get_object_or_404(Seller, pk=pk)
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def products_view(request):

    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductHyperlinkedSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def single_product_view(request, pk):

    if request.method == "GET":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    if request.method == "DELETE":
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response("Product deleted")
    if request.method == "PUT":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
