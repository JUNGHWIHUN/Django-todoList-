from django.contrib import admin
from .models import Todo
from .models import CollectedReview


# @admin.register(Todo) + 클래스 방식
@admin.register(Todo)  # 둘중 택1 둘다 있으면 오류가 발생합니다.
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )


@admin.register(CollectedReview)
class CollectedReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "review")
