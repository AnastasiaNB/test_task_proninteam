from django.db.models import Sum
from rest_framework import serializers

from deals.models import Deal, User


class TopFiveSerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()
    gems = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'spent_money', 'gems')

    def get_gems(self, obj):
        return set([deal.item.gem_name for deal in obj.deals.all()])

    def get_spent_money(self, obj):
        spent_money = Deal.objects.filter(customer=obj).aggregate(
            Sum('total')
        )['total__sum']
        return spent_money if spent_money else 0

