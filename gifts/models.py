# Django imports
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Gift(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(limit_value=0.00)])
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "brand"], name="unique_gift_and_brand")
        ]

    @property
    def in_stock_qty(self) -> int:
        return self.inventory.quantity

    def __str__(self):
        return f"{self.name} ({self.brand.name})"


class Inventory(models.Model):
    gift = models.OneToOneField(to=Gift, on_delete=models.RESTRICT)
    quantity = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], default=0)

    def __str__(self):
        return f"{self.gift.name.title()} - Inventory"


class GiftList(models.Model):
    GIFT_STATE_CHOICES = (
        ("purchased", "Purchased"),
        ("notpurchased", "Not Purchased")
    )

    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    gift = models.ForeignKey(to=Gift, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=GIFT_STATE_CHOICES, default="notpurchased")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "gift"], name="unique_user_gift_list")
        ]


@receiver(post_save, sender=Gift)
def add_initial_inventory_for_new_gift(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(gift=instance)
