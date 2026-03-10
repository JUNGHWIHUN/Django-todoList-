from rest_framework.serializers import ModelSerializer
from .models import Todo
from rest_framework import serializers
from interaction.models import TodoLike, TodoBookmark, TodoComment


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Todo

        read_only_fields = ["user"]  # 읽기만 가능

        fields = [
            # 기본 Todo 필드
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "image",
            "created_at",
            # 사용자 정보
            "user",
            "username",
            # 좋아요 관련
            "like_count",
            "is_liked",
            # 북마크 관련
            "bookmark_count",
            "is_bookmarked",
            # 댓글 수
            "comment_count",
        ]

    def _user(self):

        # serializer context에서 request 가져오기
        request = self.context.get("request")

        # 로그인 상태 확인
        if request and request.user.is_authenticated:
            return request.user

        # 로그인 안 된 경우
        return None

    def get_like_count(self, obj):

        # TodoLike 테이블에서
        # 해당 todo의 좋아요 개수 계산
        return TodoLike.objects.filter(todo=obj).count()

    # -----------------------------------------------------
    # 현재 사용자가 좋아요 눌렀는지 여부
    # -----------------------------------------------------
    def get_is_liked(self, obj):

        # 현재 로그인 사용자
        user = self._user()

        # 로그인 안한 경우
        if not user:
            return False

        # 좋아요 존재 여부 확인
        return TodoLike.objects.filter(todo=obj, user=user).exists()

    # -----------------------------------------------------
    # 북마크 개수 계산
    # -----------------------------------------------------
    def get_bookmark_count(self, obj):

        return TodoBookmark.objects.filter(todo=obj).count()

    # -----------------------------------------------------
    # 현재 사용자가 북마크 했는지 여부
    # -----------------------------------------------------
    def get_is_bookmarked(self, obj):

        # 현재 사용자
        user = self._user()

        if not user:
            return False

        return TodoBookmark.objects.filter(todo=obj, user=user).exists()

    # -----------------------------------------------------
    # 댓글 개수 계산
    # -----------------------------------------------------
    def get_comment_count(self, obj):

        return TodoComment.objects.filter(todo=obj).count()
