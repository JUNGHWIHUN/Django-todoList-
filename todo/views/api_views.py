from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

# 인증된 사용자만 접근 가능하도록 하는 권한 클래스
from rest_framework.permissions import IsAuthenticated
from ..models import Todo
from ..serializers import TodoSerializer
from rest_framework.pagination import PageNumberPagination
from interaction.models import TodoLike, TodoBookmark, TodoComment
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class TodoListAPI(APIView):
    pass


class TodoCreateAPI(APIView):
    pass


class TodoRetrieveAPI(APIView):
    pass


class TodoUpdateAPI(APIView):
    pass


class TodoDeleteAPI(APIView):
    pass


# ---------------------------------------------------------
# Todo 목록 페이지네이션 설정
# ---------------------------------------------------------
class TodoListPagination(PageNumberPagination):

    page_size = 3
    # 한 페이지에 기본적으로 보여줄 데이터 개수

    page_size_query_param = "page_size"
    # URL 쿼리 파라미터로 페이지 크기 변경 가능
    # 예: /todo/viewsets/view/?page_size=5

    max_page_size = 50
    # 사용자가 설정할 수 있는 최대 페이지 크기 제한
    # 예: page_size=100 요청 시 최대 50까지만 허용


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all().order_by("-created_at")

    serializer_class = TodoSerializer

    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):

        qs = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(qs)

        if page is not None:

            serializer = self.get_serializer(
                page,
                many=True,
                context={"request": request},
            )

            return Response(
                {
                    "data": serializer.data,
                    "current_page": int(request.query_params.get("page", 1)),
                    "page_count": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link() is not None,
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )

        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):

        todo = self.get_object()

        user = request.user

        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        if created:
            liked = True

        else:
            obj.delete()
            liked = False

        like_count = TodoLike.objects.filter(todo=todo).count()

        return Response({"liked": liked, "like_count": like_count})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):

        todo = self.get_object()

        user = request.user

        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        if created:
            bookmarked = True

        else:
            obj.delete()
            bookmarked = False

        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()

        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):

        todo = self.get_object()

        user = request.user

        content = (request.data.get("content") or "").strip()

        if not content:
            return Response({"detail": "content is required"}, status=400)

        TodoComment.objects.create(todo=todo, user=user, content=content)

        comment_count = TodoComment.objects.filter(todo=todo).count()

        return Response({"comment_count": comment_count})
