from . import BaseAPITestCase


class TestUserProfile(BaseAPITestCase):
    def test_it_creates_a_profile_whenever_a_user_is_created(self):
        response = self.create_user()
        self.authenticate()
        response = self.client.get(
            "/api/profile/{}".format(response.data['username'])
        )
        self.assertEqual(response.status_code, 200)

    def test_returns_403_when_updating_others_profile(self):
        user = self.create_user()
        # authenticate using a diffrent user
        self.authenticate(dict(
            email="a@example.com",
            username="krm",
            password="pass")
        )
        response = self.client.patch(
            f"/api/profile/{user.data['username']}",
            {"bio": "Some biography about you"}
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_update_profile(self):
        user = self.authenticate()
        response = self.client.patch(
            f"/api/profile/{user.username}",
            {"bio": "Updated bio"}
        )
        self.assertEqual(response.data['bio'], 'Updated bio')

    def test_user_cannot_update_username_through_profile_enpoint(self):
        user = self.authenticate()
        response = self.client.patch(
            f"/api/profile/{user.username}",
            {"username": "Some other user name"}
        )
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_only_see_profiles_if_authenticated(self):
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 403)

    def test_user_can_see_profiles_if_authenticated(self):
        self.authenticate()
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
