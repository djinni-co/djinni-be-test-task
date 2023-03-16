from django.http import HttpResponse

from wishlist.core import render_macro
from django.views.generic import ListView, View
from .models import Item, WishItem, WishCategory


class ItemView(ListView):
    template_name = 'index.html'
    context_object_name = 'items'
    queryset = Item.objects.prefetch_related('wishlists').prefetch_related('wishlists__category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = WishCategory.objects.all()
        return context


class WishItemView(View):

    def post(self, request):
        """Toggle view for wishlisting items"""
        pk = request.POST.get('id')
        if not pk:
            return HttpResponse('id parameter is required', 'text/plain', 400)
        macro = 'card'
        context = {}

        category_pk = request.POST.get('categoryId')
        if category_pk:
            # if it's a call with category we must render other macro
            macro = 'wish_category'
            category = WishCategory.objects.get(pk=category_pk)
            context['category'] = category

        # delete returns number of deleted items, so we can check for zero
        if not WishItem.objects.filter(item_id=pk, category_id=category_pk).delete()[0]:
            WishItem(item_id=pk, category_id=category_pk).save()

        item = Item.objects.prefetch_related('wishlists').prefetch_related('wishlists__category').get(pk=pk)
        context['item'] = item

        return render_macro(request, 'index.html', macro,
                            **context)


class WishCategoryCreateView(View):

    def post(self, request):
        name = request.POST.get('name')
        item_pk = request.POST.get('itemId')
        if not name:
            return HttpResponse('name parameter is required', 'text/plain', 400)
        
        category = WishCategory.objects.create(name=name)
        item = Item.objects.prefetch_related('wishlists').get(pk=item_pk)
        return render_macro(request, 'index.html', 
                            'wish_category', category=category, item=item)

