from django.shortcuts import render
from django.http import HttpResponse

from wishlist.core import render_macro

from .models import Item, WishItem, ItemWishList
from .validation import validate_request


def index(request):
    items = Item.objects.prefetch_related('wishlists').all()
    wish_lists = ItemWishList.objects.all()
    return render(request, 'index.html', {
        'items': items,
        'wish_lists': wish_lists
    })


def toggle_wish(request):
    resp = validate_request(request)
    if resp is not None:
        return resp
    pk = request.POST.get('id')

    # delete returns number of deleted items, so we can check for zero
    if not WishItem.objects.filter(item_id=pk).delete()[0]:
        WishItem(item_id=pk).save()

    item = Item.objects.prefetch_related('wishlists').get(pk=pk)
    return render_macro(
        request, 'index.html', 'card',
        extra_ctx={'wish_lists': ItemWishList.objects.all()},
        item=item)


def _extract_checked_wishlists(request) -> list[str]:
    prefix = 'wishlist-'
    return [
        k.removeprefix(prefix) for k, v in request.POST.items()
        if isinstance(k, str) and k.startswith(prefix) and 'on' in v
    ]


def toggle_wish_detailed(request):
    resp = validate_request(request)
    if resp is not None:
        return resp

    pk = request.POST.get('id')
    checked_wishlists = _extract_checked_wishlists(request)
    item = Item.objects.prefetch_related('wishlists', 'categories').get(pk=pk)
    item.categories.set(ItemWishList.objects.filter(pk__in=checked_wishlists))
    item.save()
    return HttpResponse('', 200)


def add_wishlist(request):
    resp = validate_request(request)
    if resp is not None:
        return resp

    new_list_name = request.POST.get('new_list_name')
    if not new_list_name:
        return HttpResponse('new_list_name parameter is required', 'text/plain', 400)
    ItemWishList(name=new_list_name).save()

    # NOTE: Can be done, using django-httpx, but since we only need one header
    #       in response, probably it's better to just add it manually
    return HttpResponse(headers={'HX-Refresh': 'true'})
