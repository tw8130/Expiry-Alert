from django.urls import path
from .views import (
    ItemListAPIView,
    ItemCreateAPIView,
    ItemDetailAPIView,
    set_preferences,
    scan_barcode,
    perform_ocr, google_auth_verify,
)

urlpatterns = [
    path('items/', ItemListAPIView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailAPIView.as_view(), name='item-detail'),
    path('items/create/', ItemCreateAPIView.as_view(), name='item-create'),
    path('items/create', ItemCreateAPIView.as_view(), name='item-create-no-slash'),
    path('preferences/', set_preferences, name='set-preferences'),
    path('scan/barcode/', scan_barcode, name='scan-barcode'),
    path('perform/ocr/', perform_ocr, name='perform-ocr'),
    # path('auth/login/', LoginView.as_view(), name='login'),
    # path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/google-verify/', google_auth_verify, name='google-auth-verify')
]
