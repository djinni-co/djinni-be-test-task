from urllib.parse import quote
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)

    @property
    def pic(self):
        return "https://picsum.photos/seed/%s/600/600" % quote(self.name)


class WishList(models.Model):
    name = models.CharField(max_length=255)
    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, related_name='lists', null=True)
