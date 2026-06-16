from rest_framework.routers import DefaultRouter
from .api import JournalEntryViewSet

router = DefaultRouter()
router.register(r'entries', JournalEntryViewSet, basename='entry')

urlpatterns = router.urls
