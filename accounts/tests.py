import pytest
from rest_framework.test import APIClient
from accounts.models import User


@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    # Create admin (lead)
    admin = User.objects.create_user(
        email="admin@test.com",
        password="Admin@123",
        role="ADMIN",
        location="HYDERABAD"
    )

    data = {
        "email": "testuser@test.com",
        "password": "Test@123",
        "role": "USER",
        "location": "HYDERABAD",
        "lead": admin.id   # ✅ IMPORTANT
    }

    response = client.post("/api/register/", data)

    assert response.status_code == 201