from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Todo


class TodoAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # 유저 생성
        self.user = User.objects.create_user(username="testuser", password="test1234")

        # JWT 토큰 발급 + 인증 헤더 설정
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

        self.todo = Todo.objects.create(
            name="운동",
            description="스쿼트 50회",
            complete=False,
            exp=10,
            user=self.user,
        )

    def test_list(self):
        res = self.client.get("/todo/viewsets/view/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json()["results"], list)

    def test_create(self):
        payload = {
            "name": "공부",
            "description": "DRF",
            "complete": False,
            "exp": 5,
        }
        res = self.client.post("/todo/viewsets/view/", payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Todo.objects.count(), 2)

    def test_retrieve(self):
        res = self.client.get(f"/todo/viewsets/view/{self.todo.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "운동")

    def test_update_patch(self):
        payload = {"name": "운동(수정)"}
        res = self.client.patch(
            f"/todo/viewsets/view/{self.todo.id}/", payload, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, "운동(수정)")

    def test_delete(self):
        res = self.client.delete(f"/todo/viewsets/view/{self.todo.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_not_found_returns_404(self):
        res = self.client.get("/todo/viewsets/view/999999/")
        self.assertEqual(res.status_code, 404)
