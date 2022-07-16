from rest_framework import serializers

from brand.models import Plan, Promotion


class PlanReadOnlySerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    amount_options = serializers.SerializerMethodField()
    tenure_options = serializers.SerializerMethodField()
    benefit_type = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ('id', 'name', 'amount_options', 'tenure_options', 'benefit_type', 'benefit_percentage')

    def get_amount_options(self, obj):
        return obj.get_amount_options_display()

    def get_tenure_options(self, obj):
        return obj.get_tenure_options_display()

    def get_benefit_type(self, obj):
        return obj.get_benefit_type_display()


class PromotionReadOnlySerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    promotion_type = serializers.SerializerMethodField()
    plan = PlanReadOnlySerializer(read_only=True)

    class Meta:
        model = Promotion
        fields = (
            'id', 'plan', 'name', 'code', 'promotion_type', 'redeemable_user', 'valid_from', 'valid_to', 'is_active')

    def get_promotion_type(self, obj):
        return obj.get_promotion_type_display()
