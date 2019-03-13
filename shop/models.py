from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS = (
    ("Rec.", "Received", ),
    ("Proc.", "Processed", ),
    ("Tran.", "Transmitted", ),
)


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, verbose_name="URL")
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    photo = models.ImageField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Order(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_client = models.CharField(max_length=150)
    adress_client = models.CharField(max_length=250)
    comment = models.TextField(max_length=700, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return "Order {}".format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])

    class Meta:
        unique_together = ('order', 'product',)

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)

    def cost(self):
        quantity = self.quantity if self.quantity else 0
        price = self.product.price if self.product.price else 0
        return price * quantity
