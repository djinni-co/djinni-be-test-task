from django.shortcuts import render
from django.http import HttpResponse

from wishlist.core import render_macro
from .models import Item, WishList


def index(request):
    items = Item.objects.all()
    return render(request, 'index.html', {
        'items': items
    })


def get_wishlists(request):
    item_id = request.GET.get('item_id')
    wishlists = WishList.objects.all()
    return render_macro(request, 'macro/wishlist_form.html', 'wishlist_form',
                        wishlists=wishlists, item_id=item_id)


def update_wishlists(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', 'text/plain', 405)

    selected_wishlists = request.POST.getlist('wishlist_set')
    item_id = request.POST.get('item_id')
    if not item_id:
        return HttpResponse('No item ID found', 'text/plain', 404)

    item = Item.objects.get(pk=item_id)
    
    wishlists = WishList.objects.all()
    # add item reference to selected wishlists
    wishlists.filter(pk__in=selected_wishlists).update(item=item)
    # remove item reference if wishlist was deselected
    wishlists.filter(item=item).exclude(
        pk__in=selected_wishlists).update(item=None)

    return render_macro(request, 'macro/wishlist_form.html', 'wishlist_form',
                        wishlists=wishlists, item_id=item_id)


def create_wishlist(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', 'text/plain', 405)

    name = request.POST.get('name')
    item_id = request.POST.get('item_id')
    if not name:
        return HttpResponse('Wishlist name is required', 'text/plain', 400)

    WishList(name=name).save()

    wishlists = WishList.objects.all()
    return render_macro(request, 'macro/wishlist_form.html', 'wishlist_form',
                        wishlists=wishlists, item_id=item_id)
