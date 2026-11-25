from django.test import TestCase
from django.urls import reverse

from .models import Utilisateur


class RegistrationViewTests(TestCase):
    def test_registration_creates_account_and_redirects_to_login(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "nouveau",
                "email": "nouveau@gmail.com",
                "telephone": "12345678",
                "role": "transporteur",
                "password1": "StrongPassword!837",
                "password2": "StrongPassword!837",
            },
        )

        self.assertRedirects(response, reverse("login"))
        user = Utilisateur.objects.get(username="nouveau")
        self.assertEqual(user.role, "transporteur")
        self.assertTrue(user.check_password("StrongPassword!837"))

    def test_registration_does_not_allow_admin_role(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "nonadmin",
                "email": "nonadmin@gmail.com",
                "role": "Admin",
                "password1": "StrongPassword!837",
                "password2": "StrongPassword!837",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Utilisateur.objects.filter(username="nonadmin").exists())
