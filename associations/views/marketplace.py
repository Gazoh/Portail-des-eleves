import json

from django.http import JsonResponse
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework import viewsets, filters

from associations.models import Marketplace, Order, Product, User
from associations.serializers import MarketplaceSerializer, OrderSerializer, ProductSerializer


class MarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status', 'buyer')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Order.objects.all().order_by("-id")

        marketplace = self.request.query_params.get('marketplace', None)
        if marketplace is not None:
            queryset = queryset.filter(product__marketplace__id=marketplace)

        return queryset

    def create(self, request, **kwargs):

        body = json.loads(request.body)
        user_id = body["user"] if "user" in body else None
        products = body["products"]

        orders, errors = [], []

        for product in products:

            quantity = int(product["quantity"])
            product = Product.objects.get(pk=product["id"])

            if quantity > product.number_left >= 0:
                errors.append({
                    product.id: "Il n'y a pas assez de {} ({} demandés, {} restants {})".format(product.name, quantity,
                                                                                                product.number_left)
                })
                continue

            status = "ORDERED"
            user = request.user
            if user_id:
                user = User.objects.get(id=user_id)
                status = "DELIVERED"

            order = Order(
                product=product,
                buyer=user,
                quantity=quantity,
                value=quantity * product.price,
                status=status
            )

            product.number_left -= quantity

            orders.append(order)

        if len(errors) >= 1:
            return JsonResponse(errors)

        for order in orders:
            order.save()
            order.product.save()

        return JsonResponse(OrderSerializer(orders, many=True).data, safe=False)
