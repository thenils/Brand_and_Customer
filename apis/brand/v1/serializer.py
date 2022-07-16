from rest_framework import serializers
from brand.models import Plan, Promotion

from apis.plans.v1.serializer import PromotionReadOnlySerializer
from apps.custom_fields import BENEFIT_CHOICES, TENURE_CHOICES, AMOUNT_CHOICES, TENURE_OPTIONS, BENEFIT_OPTIONS, \
    AMOUNT_OPTIONS, PROMOTION_CHOICES, PROMOTION_OPTIONS


class PlanReadOnlySerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    amount_options = serializers.SerializerMethodField()
    tenure_options = serializers.SerializerMethodField()
    benefit_type = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            'id', 'brand', 'name', 'description', 'amount_options', 'tenure_options', 'benefit_type',
            'benefit_percentage')

    def get_amount_options(self, obj):
        return obj.get_amount_options_display()

    def get_tenure_options(self, obj):
        return obj.get_tenure_options_display()

    def get_benefit_type(self, obj):
        return obj.get_benefit_type_display()


class PlanDetailsSerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    amount_options = serializers.SerializerMethodField()
    tenure_options = serializers.SerializerMethodField()
    benefit_type = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            'id', 'brand', 'name', 'description', 'amount_options', 'tenure_options', 'benefit_type',
            'benefit_percentage')
        read_only_fields = fields

    def get_amount_options(self, obj):
        return obj.get_amount_options_display()

    def get_tenure_options(self, obj):
        return obj.get_tenure_options_display()

    def get_benefit_type(self, obj):
        return obj.get_benefit_type_display()


class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        exclude = ['brand', 'createdAt', 'updatedAt', ]


    def validate(self, attrs):
        """
            Validate the request data

        """
        amount_options = attrs['amount_options']
        tenure_options = attrs['tenure_options']
        benefit_type = attrs['benefit_type']

        if amount_options not in AMOUNT_OPTIONS:
            raise serializers.ValidationError({
                "amount_options": f'{amount_options} is not a valid choice.',
                "valid_choice": AMOUNT_CHOICES
            })
        if tenure_options not in TENURE_OPTIONS:
            raise serializers.ValidationError({
                "tenure_options": f'{tenure_options} is not a valid choice.',
                "valid_choice": TENURE_CHOICES
            })
        if benefit_type not in BENEFIT_OPTIONS:
            raise serializers.ValidationError({
                "benefit_type": f'{benefit_type} is not a valid choice.',
                "valid_choice": BENEFIT_CHOICES
            })
        return super().validate(attrs)

    def create(self, validated_data):
        """
            Create a new Plan
        """
        request = self.context.get('request')

        if not hasattr(request.user, 'brand'):
            raise serializers.ValidationError('User must have Brand to create Plan')
        validated_data['brand']  = request.user.brand
        return Plan.objects.create(**validated_data)

class PromotionDetailSerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    promotion_type = serializers.SerializerMethodField()
    plan = PlanReadOnlySerializer(read_only=True)
    class Meta:
        model = Promotion
        fields = '__all__'

    def get_promotion_type(self, obj):
        return obj.get_promotion_type_display()


class PromotionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        exclude = ['plan','createdAt', 'updatedAt']

    def validate(self, attrs):
        """
            Validate the request data

        """
        promotion_type = attrs.get('promotion_type', None)

        if promotion_type not in PROMOTION_OPTIONS:
            raise serializers.ValidationError({
                "promotion_options": f'{promotion_type} is not a valid choice.',
                "valid_choice": PROMOTION_CHOICES
            })
        return super().validate(attrs)

    def create(self, validated_data):
        plan_id = self.context['plan_id']
        brand_plan = self.get_plan(plan_id)
        validated_data['plan'] = brand_plan
        return Promotion.objects.create(**validated_data)

    @staticmethod
    def get_plan(plan_id):
        return Plan.objects.get(id=plan_id)

