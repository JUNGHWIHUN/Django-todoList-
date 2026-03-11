from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# 현재 앱의 모델과 Serializer import
from .models import CollectedReview
from .serializers import CollectedReviewSerializer


class CollectedReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    데이터 확인용 API ViewSet

    ReadOnlyModelViewSet
    → 읽기 전용 ViewSet
    → 아래 API만 자동 생성됨

    GET /reviews/        : 리뷰 목록 조회 (list)
    GET /reviews/{id}/   : 리뷰 상세 조회 (retrieve)
    """

    queryset = CollectedReview.objects.all().order_by("-id")

    serializer_class = CollectedReviewSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
