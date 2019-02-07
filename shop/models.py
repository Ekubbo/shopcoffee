from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS = (
    ("Пол.", "Получено", ),
    ("Обр.", "Обработано", ),
    ("Отп.", "Отправлено", ),
)


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    photo = models.ImageField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        unique_slug = slugify(self.name)
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(unique_slug, num)
            num += 1
        return unique_slug


class Order(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_client = models.CharField(max_length=150)
    adress_client = models.CharField(max_length=250)
    comment = models.CharField(max_length=700, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])

    def save(self, *args, **kwargs):
        self.price = self.product.price
        models.Model.save(self, *args, **kwargs)

    def cost(self):
        quantity = self.quantity
        price = 0

        if self.price:
            price = self.price

        return price * quantity
