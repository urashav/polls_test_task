from rest_framework.routers import SimpleRouter

from surveys.views import ActiveSurveysViewSet, ResultViewSet

router = SimpleRouter()

router.register(r'survey', ActiveSurveysViewSet, basename='survey')
router.register(r'result', ResultViewSet, basename='result')
