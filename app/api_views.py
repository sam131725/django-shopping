from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Product, Category, Cart
from .serializers import ProductSerializer, CategorySerializer, CartSerializer

class ProductListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        # pass context for absolute URL resolution
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CSRFTokenAPIView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        # We also return it in the json just in case, though the cookie is the important part
        return Response({"csrfToken": get_token(request)}, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"success": True, "user": {"id": user.id, "username": user.username}}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]  # Can be called by unauthenticated or authenticated

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": True, "message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"isAuthenticated": True, "user": {"id": request.user.id, "username": request.user.username}}, status=status.HTTP_200_OK)
        return Response({"isAuthenticated": False, "user": None}, status=status.HTTP_200_OK)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user)

        serializer = CartSerializer(
            carts,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAddAPIView(APIView):
    """Add a product to the logged-in user's cart, or bump its quantity if it's already there."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1},
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart_item, context={'request': request})
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class CartItemAPIView(APIView):
    """Increment / decrement / remove a single cart line, addressed by its Cart id.

    A decrement that would take quantity to zero deletes the row instead,
    matching the behaviour of the (fixed) template-based minus_cart view.
    """
    permission_classes = [IsAuthenticated]

    def _get_item(self, request, pk):
        # Scoped to request.user so one account can never touch another's cart row.
        return Cart.objects.filter(pk=pk, user=request.user).first()

    def patch(self, request, pk, *args, **kwargs):
        item = self._get_item(request, pk)
        if not item:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'increment':
            item.quantity += 1
            item.save()
        elif action == 'decrement':
            if item.quantity <= 1:
                item.delete()
                return Response({'deleted': True}, status=status.HTTP_200_OK)
            item.quantity -= 1
            item.save()
        else:
            return Response(
                {'error': "action must be 'increment' or 'decrement'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CartSerializer(item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        item = self._get_item(request, pk)
        if not item:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)