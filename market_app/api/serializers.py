from rest_framework import serializers
from market_app.models import Market, Product, Seller


def validate_positive_value(value):
    if value < 0:
        raise serializers.ValidationError("Net worth must be a positive value.")
    return value


class MarketSerializer(serializers.ModelSerializer):
    sellers = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="seller-detail")
    products = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="product-detail")

    class Meta:
        model = Market
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value


class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Market
        fields = ['id', 'name', 'location', 'url', 'description', 'net_worth', 'sellers', 'products']


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), many=True, write_only=True, source="markets")

    class Meta:
        model = Seller
        fields = '__all__'


class SellerHyperlinkedSerializer(SellerSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        exclude = []


class ProductSerializer(serializers.ModelSerializer):
    market = MarketHyperlinkedSerializer(read_only=True)
    seller = SellerHyperlinkedSerializer(read_only=True)
    market_id = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), write_only=True, source="market")
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, source="seller")

    class Meta:
        model = Product
        fields = '__all__'


class ProductHyperlinkedSerializer(ProductSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        exclude = []
