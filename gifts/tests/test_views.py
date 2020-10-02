# Django imports
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.management import call_command

# Project imports
from gifts.models import Gift
from gifts.models import GiftList
from gifts.models import Guest


class ViewsTestCases(TestCase):
    PASSWORD = "secret"

    def setUp(self) -> None:
        # Let's add some data
        call_command("prepare")

        # Let's add a user
        self.user = User.objects.create(
            email="user@bla.bla",
            username="user",
            password=ViewsTestCases.PASSWORD
        )

        # Let's get a product
        self.product = Gift.objects.get(name="Cast Iron Oval Casserole - 25cm; Volcanic")

    def test_show_all_gifts(self):
        c = Client()
        c.request(user=self.user)
        c.force_login(self.user)

        res = c.get("/api/v1/gifts")

        self.assertEqual(res.status_code, 200)

    def test_add_guest(self):
        c = Client()
        c.request(user=self.user)
        c.force_login(self.user)

        data = {
            "first_name": "otto",
            "last_name": "Schuldt",
            "username": "ottosg",
            "password": "secret",
            "user_id": self.user.id
        }
        res = c.post("/api/v1/guests", data=data)

        # response should be 200
        self.assertEqual(res.status_code, 200)

        # let's check if guest was created
        guest_qs = User.objects.filter(username="ottosg")
        self.assertTrue(guest_qs.exists())

        # Let's check if new user is a guest
        guest = guest_qs.get()

        self.assertTrue(hasattr(guest, "guest"))

    def test_get_wedding_list(self):
        # Let's create a fake wedding list for user
        GiftList.objects.create(
            user=self.user,
            gift=self.product
        )

        c = Client()
        c.request(user=self.user)
        c.force_login(self.user)

        res = c.get("/api/v1/wedding-list?user_id=%s" % self.user.id)

        # response should be 200.
        self.assertEqual(res.status_code, 200)

        # response data should contain info of the recent added gift...
        res_data = res.json()
        self.assertTrue(res_data["user_id"] == self.user.id)
        self.assertTrue(res_data["gifts"][0]["gift_id"] == self.product.id)

    def test_purchase_gift(self):
        # Let's create a fake wedding list for user
        GiftList.objects.create(
            user=self.user,
            gift=self.product
        )

        # Let's add a guest
        user_guest = User.objects.create(
            username="bla",
            password=ViewsTestCases.PASSWORD,
        )

        Guest.objects.create(user=user_guest, inviter=self.user)

        c = Client()
        c.request(user=user_guest)
        c.force_login(user_guest)

        res = c.post("/api/v1/wedding-list", data={
            "gift_id": self.product.id,
            "user_id": self.user.id,
        })

        self.assertTrue(res.status_code, 200)

    def test_remove_gift_from_wedding_list(self):
        # Let's create a fake wedding list for user
        GiftList.objects.create(
            user=self.user,
            gift=self.product
        )

        c = Client()
        c.request(user=self.user)
        c.force_login(self.user)

        res = c.delete("/api/v1/wedding-list", data={
            "gift_id": self.product.id,
            "user_id": self.user.id,
        })

        self.assertTrue(res.status_code, 200)
