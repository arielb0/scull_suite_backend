from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wimm.permissions import IsOwner
from wimm.serializers import AccountSerializer, ConfigurationSerializer, SummarySerializer, TransactionSerializer
from wimm.models import Account, Configuration, Transaction
from wimm.selectors import get_accounts, get_last_transactions, get_total_amount, get_total_budget, get_summary
from wimm.services import apply_budget


class AccountViewSet(ModelViewSet):
    
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class TransactionViewSet(ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-timestamp')


class ConfigurationView(GenericAPIView):

    serializer_class = ConfigurationSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        configuration, created = Configuration.objects.get_or_create(
            user=self.request.user,
            defaults={
                'currency': 'USD', 
                'currency_display': 'symbol',
                'locale': 'en-EN'
            }
        )
        serializer = self.get_serializer(configuration)
        return Response(serializer.data)    
    
    def put(self, request, *args, **kwargs):
        try:
            configuration = Configuration.objects.get(user=self.request.user)
            configuration.locale = self.request.data['locale']
            configuration.currency = self.request.data['currency']
            configuration.save()
            serializer = self.get_serializer(configuration)
            return Response(serializer.data)
        except:
            raise NotFound


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({
            'total_amount': get_total_amount(self.request.user),
            'total_budget': get_total_budget(self.request.user),
            'accounts': get_accounts(self.request.user),
            'last_transactions': get_last_transactions(self.request.user)
        })


class ApplyBudgetView(APIView):

    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, format=None):
        
        if 'source_account' in self.request.data: # Check if user is the owner of source_account
            try:
                self.check_object_permissions(request, Account.objects.get(pk=self.request.data['source_account']))
                apply_budget(self.request.user, Account.objects.get(pk=self.request.data['source_account']))
            except Exception as message:
                return Response({'detail': message.__str__()}, status=422)
            
            return Response({'detail': 'Budget applied successfully'})
        
        return Response({'detail': 'You need to provide source_account parameter'}, status=422)

        
class SummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, account_id: int, format=None):
        try:
            self.check_object_permissions(request, Account.objects.get(pk=account_id))
            summaries = get_summary(self.request.user, account_id) # Check if user has permission to get the summary of account_id
            serializer = SummarySerializer(summaries, many=True)
            return Response(serializer.data)
        except:
            return Response({'detail': 'You need to provide a valid account_id parameter'}, status=404)