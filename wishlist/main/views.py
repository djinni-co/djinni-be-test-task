from django.shortcuts import render
from django.http import HttpResponse

from wishlist.core import render_macro
from .models import Item, WishItem


def index(request):
    items = Item.objects.prefetch_related('wishlists').all()
    return render(request, 'index.html', {
        'items': items
    })


def toggle_wish(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', 'text/plain', 400)

    pk = request.POST.get('id')
    if not pk:
        return HttpResponse('id parameter is required', 'text/plain', 400)

    # delete returns number of deleted items, so we can check for zero
    if not WishItem.objects.filter(item_id=pk).delete()[0]:
        WishItem(item_id=pk).save()

    item = Item.objects.prefetch_related('wishlists').get(pk=pk)
    return render_macro(request, 'index.html', 'card',
                        item=item)
