from django.db import models

from positions.fields import PositionField


class Product(models.Model):
    name = models.CharField(max_length=50)


    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='ProductCategory', related_name='categories')

    def __unicode__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = PositionField(collection='category')

    class Meta(object):
        unique_together = ('product', 'category')

    def __unicode__(self):
        return u"%s in %s" % (self.product, self.category)
