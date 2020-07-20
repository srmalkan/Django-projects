from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Item,OrderItem,Order,BillingAddress
from django.utils import timezone
from django.views.generic import ListView,DetailView,View
from .forms import UserRegistrationForm,ReviewsForm,CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# stripe payment
import stripe
stripe.api_key = "sk_test_51H3flKFdEDGoP81seITo40R47EedM4GHnz6rOwiszzoQg6z8rXmTd1ll2jvNk7ingf5aVK02K9TlkpxxfTzXhWz500rPH98WYT"

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
        # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
        # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
        # Save the User object
            new_user.save()
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form})

class ItemList(ListView):
    model = Item
    context_object_name = 'items'
    paginate_by = 8
    template_name='itemList.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'slug' in self.kwargs:
            print(self.kwargs['slug'])
            if self.kwargs['slug']!='all':
                print(self.kwargs['slug'])
                qs = qs.filter(itemCategory=self.kwargs['slug'])
        return qs
    

class ItemDetail(DetailView):
    model = Item
    template_name='item.html'
    context_object_name = 'item'

    def get_object(self):
        obj = get_object_or_404(Item,itemSlug = self.kwargs['itemSlug'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ReviewsForm()
        reviews = self.get_object().reviews.all()
        context["form"] = form
        context["reviews"] = reviews
        return context
    
    def post(self,request,*args,**kwargs):
        Review_form = ReviewsForm(request.POST)
        if Review_form.is_valid():
            review = Review_form.save(commit=False)
            review.user = request.user
            review.item = self.get_object()
            review.save()
            return redirect(reverse("core:itemDetail", kwargs={"itemSlug": self.get_object().itemSlug}))
 
@login_required
def add_to_cart(request,id):
    item = get_object_or_404(Item,id=id)
    user = request.user
    order_qs = user.orders.all().filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        print(order_items)
        for oitem in order_items:
            print(oitem.item.id)
        if order_items.filter(item = item).exists():
            print("order_items")
            order_item = order_items.get(item = item)
            order_item.quantity +=1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(item = item, order=order)
    else:
        order= Order.objects.create(user = user,ordered_date = timezone.now())
        order_item = OrderItem.objects.create(item = item, order=order)
        order.items.add(order_item)
    messages.success(request, "Item added to cart")
    return redirect(reverse("core:itemDetail", kwargs={"itemSlug": item.itemSlug}))

#order_item = OrderItem.objects.create(item = item)

@login_required
def remove_from_cart(request,id):
    item = get_object_or_404(Item,id=id)
    user = request.user
    order_qs = user.orders.all().filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        if order_items.filter(item = item).exists():
            order_item = order_items.get(item = item)
            if order_item.quantity==1:
                order_item.delete()
            else:
                order_item.quantity -=1
                order_item.save()
    messages.warning(request, "Item removed from cart")
    return redirect(reverse("core:itemDetail", kwargs={"itemSlug": item.itemSlug}))


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            order = request.user.orders.filter(ordered=False)[0]
            return render(self.request,'orderSummary.html',{'order':order})
        except ObjectDoesNotExist: 
            return redirect("core:itemList",slug='all')


@login_required
def add_to_order(request,id):
    order_item = get_object_or_404(OrderItem,id=id)
    order_item.quantity +=1
    order_item.save()
    return redirect(reverse("core:orderSummary"))

#order_item = OrderItem.objects.create(item = item)

@login_required
def remove_from_order(request,id):
    order_item = get_object_or_404(OrderItem,id=id)
    if order_item.quantity==1:
        order_item.delete()
    else:
        order_item.quantity -=1
        order_item.save()

    return redirect(reverse("core:orderSummary"))

@login_required
def delete_from_order(request,id):
    order_item = get_object_or_404(OrderItem,id=id)
    order_item.delete()
    return redirect(reverse("core:orderSummary"))

class CheckoutView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form =CheckoutForm()
        order = request.user.orders.all().filter(ordered=False)[0]
        return render(request,'checkout.html',{'form':form,'order':order})

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            Address_1 = cd['Address_1']
            Address_2 = cd['Address_2']
            state = cd['state']
            zipCode = cd['zipCode']
            same_billing_address = cd['same_billing_address']
            save_info = cd['save_info']
            payment_option = cd['payment_option']
            BillingAddress = BillingAddress(
                user = request.user,
                Address_1 = Address_1,
                Address_2 = Address_2,
                state = state,
                zipCode = zipCode
            )
            BillingAddress.save()
            order = request.user.orders.all().filter(ordered=False)[0]
            order.billing_address = BillingAddress
            order.save()
            return redirect(reverse("core:checkout"))

class PaymentView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        order = request.user.orders.all().filter(ordered=False)[0]
        return render(self.request,'payment/stripe.html',{'order':order})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        order = request.user.orders.all().filter(ordered=False)[0]
        charge = stripe.Charge.create(
            amount=int(order.get_grand_total()*100),
            currency="inr",
            source=request.POST['stripeToken'],
            description=f"{order.get_grand_total()} paid by {request.user.username}",
        )
        if charge.status == 'succeeded':
            return HttpResponse('Success')
        return render(self.request,'payment/stripe.html')
