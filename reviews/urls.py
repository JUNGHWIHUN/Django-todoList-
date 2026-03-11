from rest_framework.routers import DefaultRouter
from .views import CollectedReviewViewSet


router = DefaultRouter()


router.register(
    r"collected-reviews", CollectedReviewViewSet, basename="collected-reviews"
)

urlpatterns = router.urls
