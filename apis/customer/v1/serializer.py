from datetime import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from brand.models import Plan, Promotion
from customer.models import CustomerGoal

from apis.plans.v1.serializer import PlanReadOnlySerializer


class CustomerGoalReadOnlySerializer(serializers.ModelSerializer):
    plan = PlanReadOnlySerializer(read_only=True)

    class Meta:
        model = CustomerGoal
        fields = [
            'id', 'plan', 'user',
            'deposit_amount', 'createdAt', 'start_date', 'is_active'
        ]


class CustomerWOSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField(required=False)
    code = serializers.CharField(required=False)
    is_active = serializers.CharField(required=False)
    deposit_amount = serializers.IntegerField(required=False)

    def create(self, validate_data):
        with transaction.atomic():
            request = self.context['request']
            plan = None
            if 'plan_id' in validate_data:
                plan = get_object_or_404(Plan, pk=validate_data['plan_id'])

            if not plan or not plan.is_active:
                raise serializers.ValidationError('This plan is not active any more',
                                                  code=status.HTTP_406_NOT_ACCEPTABLE)
            # if CustomerGoal.objects.filter(user=request.user, plan=plan).exists():
            #     raise serializers.ValidationError('This plan is already enrolled buy you',
            #                                       code=status.HTTP_406_NOT_ACCEPTABLE)

            deposit_amount = validate_data.get('deposit_amount', 0)
            if plan and 'code' in validate_data:
                promotion = get_object_or_404(Promotion, code=validate_data['code'])
                is_valid, message = promotion.is_valid()
                if not is_valid:
                    raise serializers.ValidationError('This Promo has been fully claimed!',
                                                      code=status.HTTP_406_NOT_ACCEPTABLE)
                discount = ((deposit_amount * plan.benefit_percentage) / 100)
                deposit_amount = deposit_amount - discount
                promotion.redeemed += 1
                promotion.save()

                """
                here we can create client profile 
                and create return the discounted value to the client like wallet, deduct from payable amount
                """

            CustomerGoal.objects.create(user=request.user,
                                        plan=plan,
                                        selected_amount=plan.amount_options,
                                        selected_tenure=plan.tenure_options,
                                        benefit_type=plan.benefit_type,
                                        benefit_percentage=plan.benefit_percentage,
                                        deposit_amount=deposit_amount,
                                        start_date=datetime.now())

            return CustomerGoal

