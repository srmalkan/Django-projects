from django.urls import path
from .views import ItemList,ItemDetail,add_to_cart,remove_from_cart,register,OrderSummaryView,add_to_order,remove_from_order,delete_from_order,CheckoutView,PaymentView
app_name = 'core'
urlpatterns = [
    path("order/", OrderSummaryView.as_view(), name="orderSummary"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("item/<slug:itemSlug>/", ItemDetail.as_view(), name="itemDetail"),
    path("addtocart/<id>/",add_to_cart,name="addtocart"),
    path("removefromcart/<id>/",remove_from_cart,name="removefromcart"),
    path("addtoorder/<id>/",add_to_order,name="addtoorder"),
    path("removefromorder/<id>/",remove_from_order,name="removefromorder"),
    path("deletefromorder/<id>/",delete_from_order,name="deletefromorder"),
    path('register/',register,name='register'),
    path("home/<slug>/", ItemList.as_view(), name="itemList"),

]
