from django.urls import path
from rest_framework import routers
from .views import SummaryView, AccountViewSet, TransactionViewSet, ConfigurationView\
    , DashboardView, ApplyBudgetView

router = routers.DefaultRouter()

router.register('accounts', AccountViewSet, basename = 'accounts')
router.register('transactions', TransactionViewSet, basename = 'transactions')

urlpatterns = [
    path('dashboard', DashboardView.as_view()),
    path('configuration', ConfigurationView.as_view()),
    path('apply-budget', ApplyBudgetView.as_view()),
    path('summary/<int:account_id>/', SummaryView.as_view()),
]

urlpatterns +=  router.urls