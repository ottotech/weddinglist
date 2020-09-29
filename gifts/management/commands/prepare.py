# Python imports
import json
import os
import decimal

# Django imports
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# Project imports
from gifts.models import Brand
from gifts.models import Gift


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Let's create a superuser.
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@bla.bla",
                password="admin1234"
            )

        script_path = os.path.dirname(__file__)
        path = os.path.join(script_path, "products.json")

        # Let's create sample products.
        with open(path) as f:
            gifts = json.load(f)
            for g in gifts:

                if not Brand.objects.filter(name=g["brand"]).exists():
                    Brand.objects.create(name=g["brand"])

                if not Gift.objects.filter(name=g["name"], brand__name=g["brand"]).exists():
                    price = decimal.Decimal(g["price"].replace("GBP", ""))

                    Gift.objects.create(
                        name=g["name"],
                        brand=Brand.objects.get(name=g["brand"]),
                        price=price,
                    )
