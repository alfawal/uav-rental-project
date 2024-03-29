# myapp/management/commands/seed.py
import os
from datetime import timedelta
from io import BytesIO

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

import requests
from PIL import Image


@transaction.atomic
def create_initial_data():
    user_model = get_user_model()
    user_model.objects.create(
        username="admin",
        email="admin@uav.com",
        is_active=True,
        is_superuser=True,
        is_staff=True,
        password=make_password("admin"),
    )
    print("\n--- Created an admin user:\n\tusername: admin\n\tpassword: admin")

    new_users = []
    for username in ("customer1", "customer2"):
        new_user = user_model.objects.create(
            username=username,
            email=f"{username}@uav.com",
            is_active=True,
            is_customer=True,
            password=make_password(username),
        )
        new_users.append(new_user.id)
        print(
            f"--- Created a customer user:\n\tusername: {username}"
            f"\n\tpassword: {username}"
        )

    uav_model = apps.get_model("uav", "UAVModel")
    new_uavs = []
    for uav in (
        {
            "brand": "Baykar/Bayraktar",
            "model": "TB2",
            "weight": 70,
            "category": "MALE",
            "description": (
                "The Bayraktar TB2 is a Tactical Armed / UAV System,"
                " developed and manufactured by Baykar. A highly sophisticated"
                " design that provides all solutions that operator may need in"
                " one integrated system. The system consists of Bayraktar TB2"
                " Armed / UAV Platform, Ground Control Station, Ground Data"
                " Terminal, Remote Display Terminal, Advanced Base with"
                " Generator and Trailer modules. Thanks to Baykar's"
                " technological accumulation and capabilities, the entire"
                " system is produced indigenously."
            ),
            "daily_price": 10000,
            "photo": "https://cdn.baykartech.com/media/upload/userFormUpload/bw155mWvTOzG0bG7GNDpPbjuzyVSeHd0.png",  # noqa: E501
            "data": {
                "Max Altitude": "25.000 Feet",
                "Flight Record": "27 Hours 3 Minutes",
            },
        },
        {
            "brand": "Baykar/Bayraktar",
            "model": "Kizilelma (MIUS)",
            "weight": 1200,
            "category": "HALE",
            "description": (
                "With consideration of a future where air combat will be"
                ' dominated by unmanned technology, our "Bayraktar'
                ' KIZILELMA Fighter UAV", being developed fully within'
                " Turkish borders, will most certainly play an increasingly"
                " important role moving ahead."
            ),
            "daily_price": 50000,
            "photo": "https://cdn.baykartech.com/media/upload/userFormUpload/Hah7YHhNwyMstS6tfzJW6QW6PwvsfXQI.png",  # noqa: E501
            "data": {
                "Max Altitude": "30.000 Feet",
                "Endurance": "5 Hours",
            },
        },
    ):
        url = uav.pop("photo")
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        img_io = BytesIO()
        img.save(img_io, format="PNG")

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(img_io.getvalue())
        img_temp.flush()

        uav["photo"] = File(img_temp, name=os.path.basename(url))

        new_uav = uav_model.objects.create(**uav)
        new_uavs.append(new_uav.id)

    rental_model = apps.get_model("rental", "Rental")
    for rental in (
        {
            "user_id": new_users[0],
            "uav_id": new_uavs[0],
            "start_date": (timezone.now() - timedelta(days=5)),
            "end_date": (timezone.now() - timedelta(days=1)),
            "price": 1,
        },
        {
            "user_id": new_users[0],
            "uav_id": new_uavs[0],
            "start_date": timezone.now(),
            "end_date": (timezone.now() + timedelta(days=1)),
            "price": 1,
        },
        {
            "user_id": new_users[1],
            "uav_id": new_uavs[1],
            "start_date": (timezone.now() - timedelta(days=5)),
            "end_date": (timezone.now() + timedelta(days=4)),
            "price": 1,
        },
        {
            "user_id": new_users[1],
            "uav_id": new_uavs[1],
            "start_date": timezone.now(),
            "end_date": (timezone.now() + timedelta(days=5)),
            "price": 1,
        },
    ):
        rental_model.objects.create(**rental)


class Command(BaseCommand):
    help = "Create initial data"

    def handle(self, *args, **options) -> None:
        create_initial_data()
        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
