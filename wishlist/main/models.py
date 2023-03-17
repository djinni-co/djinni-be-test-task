from urllib.parse import quote
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)

    @property
    def pic(self):
        return "https://picsum.photos/seed/%s/600/600" % quote(self.name)


class WishItem(models.Model):
    # unique rather than OneToOne here since we forego authentication, but in a
    # real world that would be just normal FK
    item = models.ForeignKey(Item, on_delete=models.CASCADE, unique=True,
                             related_name='wishlists')


class ItemWishList(models.Model):
    name = models.CharField(max_length=255)
    # while `wishlist` is more obvious choice for a related name, it's taken
    # and to not remove something already present we got to come up with smth
    # new
    items = models.ManyToManyField(Item, related_name="categories")
