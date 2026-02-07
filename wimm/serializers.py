from rest_framework.serializers import ModelSerializer
from .models import Account, Configuration, Summary, Transaction


class AccountSerializer(ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'goal_description', 'goal_amount'
                  , 'budget_percentage', 'include_on_summary_section'
                  , 'include_on_total_amount', 'amount', 'color']
        read_only_fields = ['id', 'user', 'amount']


class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'timestamp', 'amount', 'source_account'
                  , 'destination_account', 'description'
                  , 'source_account_name', 'destination_account_name'
                  , 'keywords']
        read_only_fields = ['id', 'user', 'source_account_name'
                            , 'destination_account_name'
                            , 'keywords']

class ConfigurationSerializer(ModelSerializer):

    class Meta:
        model = Configuration
        fields = ['id', 'user', 'currency', 'currency_display', 'locale']
        read_only_fields = ['id', 'user']


class SummarySerializer(ModelSerializer):

    class Meta:
        model = Summary
        fields = ['timestamp', 'amount']