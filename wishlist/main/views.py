from django.http import HttpResponse
from django.views.generic import ListView, View
from django.http import QueryDict

from wishlist.core import render_macro, get_macro_markup
from .models import Item, WishItem


class ItemView(ListView):
    template_name = 'index.html'
    context_object_name = 'items'
    queryset = Item.objects.prefetch_related('wishlists').all()


class WishItemView(View):

    def get(self, request):
        # this function returns a contatinated list of all WishItems
        item_id = request.GET.get('item_id')
        
        wish_items = WishItem.objects.filter(item_id=item_id)
        wish_items_names = wish_items.values_list('name', flat=True)
        wish_items_unchecked = WishItem.objects.filter(item__isnull=True).exclude(name__in=list(wish_items_names))
        wish_items_list = wish_items | wish_items_unchecked
        wish_items_list_no_default = wish_items_list.exclude(name__isnull=True)

        all_macro_markup = [get_macro_markup(request, 'index.html', 'wish_item',
                            wish_item=item, item_id=item_id) for item in wish_items_list_no_default]
        concat_markup = ''.join(all_macro_markup)
        return HttpResponse(concat_markup)

    def post(self, request):
        """Creation view of WishItem, return a rendered WishItem html"""
        name = request.POST.get('name')
        item_id = request.POST.get('item_id')
        if WishItem.objects.filter(name=name).exists():
            return HttpResponse(f'WishItem with name {name} already exists!', 'text/plain', 400)

        wish_item = WishItem.objects.create(name=name)

        return render_macro(request, 'index.html', 'wish_item',
                            wish_item=wish_item, item_id=item_id)

    def put(self, request):
        """Toggle view for wishlisting items"""
        put_data = QueryDict(request.body)
        item_id = put_data.get('item_id')
        if not item_id:
            return HttpResponse('id parameter is required', 'text/plain', 400)
        
        name = put_data.get('name')

        # the delete operator returns a tuple, where the first element is how many items were deleted
        # if it's 0 then the user wishlisted the item, otherwise unwhished
        wishlisted = not WishItem.objects.filter(item_id=item_id, name=name).delete()[0]
        if wishlisted:
            wish_item = WishItem(item_id=item_id, name=name)
            wish_item.save()


        if not name:
            # in case we saved to a default wishlist, just return the checked/unchecked book mark to put in the "Save" button
            bookmark_type = '-fill' if wishlisted else ''
            return HttpResponse(f'<i class="bi bi-bookmark{bookmark_type}"></i> Save')
        
        # If the user unwhishes we return unwished item wish item
        if not wishlisted:
            wish_item = WishItem.objects.get(name=name, item__isnull=True)
        
        return render_macro(request, 'index.html', 'wish_item',
                            wish_item=wish_item, item_id=item_id)
