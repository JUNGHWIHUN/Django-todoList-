from rest_framework.serializers import ModelSerializer
from .models import Todo


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo

        read_only_fields = ["created_at", "updated_at"]  # 읽기만 가능

        fields = [
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "completed_at",
            "created_at",
            "updated_at",
            "image",
        ]
