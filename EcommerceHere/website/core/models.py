from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

CATEGORY=(
    ("cl","Clothing"),
    ("el", "Electronics"),
    ("sp", "Sports,Books & More"),
    ("hf", "Home & Furniture"),
)
# Create your models here.
class Item(models.Model):
    itemName = models.CharField(max_length=100)
    itemPrice = models.FloatField()
    itemDiscountedPrice = models.FloatField(blank=True, null=True)
    itemCategory = models.CharField(choices = CATEGORY,max_length=2)
    itemRating = models.FloatField()
    itemRatingNumber = models.IntegerField()
    itemSlug = models.SlugField()
    itemDescription = models.TextField()
    itemImage = models.ImageField()
    itemPurchases = models.IntegerField()

    class Meta:
        verbose_name = ("Item")
        verbose_name_plural = ("Items")

    def __str__(self):
        return self.itemName

    def get_absolute_url(self):
        return reverse("core:itemDetail", kwargs={"itemSlug": self.itemSlug})

    def add_to_cart_url(self):
        return reverse("core:addtocart",kwargs={"id": self.id})
    
    def remove_from_cart_url(self):
        return reverse("core:removefromcart",kwargs={"id": self.id})

    def add_to_order_url(self):
        return reverse("core:addtoorder",kwargs={"id": self.id})
    
    def remove_from_order_url(self):
        return reverse("core:removefromorder",kwargs={"id": self.id})

class Order(models.Model):
    user = models.ForeignKey(User,related_name='orders',
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey("BillingAddress", on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return self.user.username
    
    def get_grand_total(self):
        total=0
        for oitems in self.items.all():
            total+=oitems.get_total_price()
        return total
    
    def get_grand_saving(self):
        total=0
        for oitems in self.items.all():
            total+=(oitems.item.itemPrice*oitems.quantity) - oitems.get_total_price()
        return total

    

    # def get_absolute_url(self):
    #     return reverse("Order_detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")
    
    def get_total_price(self):
        if self.item.itemDiscountedPrice:
            return self.quantity * self.item.itemDiscountedPrice
        else:
            return self.quantity * self.item.itemPrice

    def add_to_order_url(self):
        return reverse("core:addtoorder",kwargs={"id": self.id})
    
    def remove_from_order_url(self):
        return reverse("core:removefromorder",kwargs={"id": self.id})

    def delete_item(self):
        return reverse("core:deletefromorder",kwargs={"id": self.id})

    # def __str__(self):
    #     return self.name

    # def get_absolute_url(self):
    #     return reverse("order_item_detail", kwargs={"pk": self.pk})

class Reviews(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

state_choices = (
    ('maharashtra','maharashtra'),
    ('gujrat','gujrat'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Rajasthan','Rajasthan'),
    ('Punjab','Punjab')
)

class BillingAddress(models.Model):

    user = models.ForeignKey(User, related_name = "billingaddress", on_delete=models.CASCADE)
    Address_1 = models.CharField(max_length=200)
    Address_2 = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(choices=state_choices,max_length = 20)
    zipCode = models.CharField(max_length = 8)
    class Meta:
        verbose_name = ("billingaddress")
        verbose_name_plural = ("billingaddresss")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("billingaddress_detail", kwargs={"pk": self.pk})

# class PaymentDetails(models.Model):
#     stripe_token = []






