from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        print(args, 111111, kwargs)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an activ order")
            return redirect("/")


@login_required
def checkout(request):
    return render(request, "checkout-page.html")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug, user=None):
    item = get_object_or_404(Item, slug=slug)
    if user is None:
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            item=item,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "The Item's quantitiy was updated")
                return redirect("core:order-summary")
            else:
                order = order.items.add(order_item)
                messages.info(request, "The Item was added to you cart")
                return redirect("core:product", slug=slug)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order = order.items.add(order_item)
            messages.info(request, "The Item was added to you cart")
            return redirect("core:product", slug=slug)
    else:
        # for Admin user
        order_item, created = OrderItem.objects.get_or_create(
            user__username=user,
            item=item,
            ordered=False
        )
        order_qs = Order.objects.filter(user__username=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "The Item's quantitiy was updated")
                return redirect(F"core:user-order-view", user=user)
            else:
                order = order.items.add(order_item)
                messages.info(request, "The Item was added to you cart")
                return redirect("core:product", slug=slug)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order = order.items.add(order_item)
            messages.info(request, "The Item was added to you cart")
            return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug, user=None):
    item = get_object_or_404(Item, slug=slug)

    if user is None:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    user=request.user,
                    item=item,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "The Item was removed from cart")
                return redirect("core:order-summary")
            else:
                # this Item isnt in list
                messages.info(request, "The item isn't in your cart")
                return redirect("core:product", slug=slug)

        else:
            # message syaing user doesn't have a cart
            messages.info(request, "You dont have any order yet")
            return redirect("core:product", slug=slug)
    else:

        order_qs = Order.objects.filter(user__username=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    user__username=user,
                    item=item,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "The Item was removed from cart")

                return redirect(F"core:user-order-view", user=user)


@login_required
def decrease_item_quantity(request, slug, user=None):
    item = get_object_or_404(Item, slug=slug)
    if user is None:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    user=request.user,
                    item=item,
                    ordered=False
                )[0]
                if order_item.quantity != 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(
                        request, "Quantity of the Item was decreased")
                else:
                    order.items.remove(order_item)
                    messages.info(request, "The Item was removed from cart")

        return redirect("core:order-summary")
    else:
        order_qs = Order.objects.filter(user__username=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    user__username=user,
                    item=item,
                    ordered=False
                )[0]
                if order_item.quantity != 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(
                        request, "Quantity of the Item was decreased")
                else:
                    order.items.remove(order_item)
                    messages.info(request, "The Item was removed from cart")

        return redirect(F"core:user-order-view", user=user)


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class OrderListView(SuperUserCheck, ListView):
    template_name = "order_list.html"

    def get_queryset(self):
        queryset = Order.objects.all().filter(ordered=False)
        return queryset


def user_order_view(request, user):

    # print(user.username)
    order = Order.objects.get(user__username=user, ordered=False)
    context = {"object": order}
    return render(request, "order_summary.html", context)
