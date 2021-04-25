from rest_framework import serializers

from store.models import Category, Product, UserBase


class ProductSerializer(serializers.ModelSerializer):
    product_creator = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()


    def get_product_creator(self, obj):
        return obj.product_creator.username

    def get_category(self, obj):
        return obj.category.name

    def get_url(self, obj):
        return obj.get_api_url

    class Meta:
        model = Product
        fields = ('pk', 'title', 'product_code', 'category', 'product_creator', 'price', 'image', 'url')


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=[category.name for category in Category.objects.all()]
    )

    product_creator = serializers.ChoiceField(
        choices=[user.username for user in UserBase.objects.all()]
    )
    
    class Meta:
        model = Product
        fields = ('title', 'product_code', 'category', 'product_creator', 'price', 'image', )


    def create(self, validated_data):
        """
        Add category and product_creator field to create view
        """

        category = Category.objects.filter(name=validated_data['category']).first()
        product_creator = UserBase.objects.filter(username=validated_data['product_creator']).first()

        validated_data['category'] = category
        validated_data['product_creator'] = product_creator

        return super().create(validated_data)


    def update(self, instance, validated_data):
        """
        Update category and product_creator field to update view
        """
        
        category = Category.objects.filter(name=validated_data['category']).first()
        product_creator = UserBase.objects.filter(username=validated_data['product_creator']).first()

        validated_data['category'] = category
        validated_data['product_creator'] = product_creator

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BasketAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)

    qty = serializers.IntegerField(min_value=1, max_value=None)


class BasketRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)


class BasketUpdateSerializer(serializers.Serializer):
    product_id = serializers.CharField()

    qty = serializers.IntegerField(min_value=1, max_value=None)

