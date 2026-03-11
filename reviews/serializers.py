from rest_framework import serializers
from .models import CollectedReview


class CollectedReviewSerializer(serializers.ModelSerializer):

    class Meta:

        model = CollectedReview

        fields = [
            "id",  # DB 기본 키 (Primary Key)
            "title",  # 리뷰 제목
            "review",  # 리뷰 본문
            "doc_id",  # 중복 방지용 문서 ID
            "collected_at",  # 데이터 수집 시각
        ]
