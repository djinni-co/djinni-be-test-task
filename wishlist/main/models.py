from urllib.parse import quote
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)

    @property
    def pic(self):
        return f"https://picsum.photos/seed/{quote(self.name)}/600/600"


class WishItem(models.Model):
    # unique rather than OneToOne here since we forego authentication, but in a
    # real world that would be just normal FK
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='wishlists', null=True)
    name = models.CharField(max_length=255, null=True)
