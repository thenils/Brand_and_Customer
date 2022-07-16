from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.custom_fields import get_default_address, AMOUNT_CHOICES, TENURE_CHOICES, BENEFIT_CHOICES, PROMOTION_CHOICES
from apps.default import BaseModel
from django.db import models


class Brand(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=55, help_text="Enter brand name eg. Apple ")
    phone = models.CharField(max_length=15, null=True, blank=True, help_text='with +cc-number')
    description = models.TextField(null=True, blank=True, help_text='optional')
    address = models.JSONField(default=get_default_address)
    website = models.URLField(null=True, blank=True, help_text='optional')

    class Meta:
        db_table = 'brand'
        app_label = 'brand'
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}.{self.name}'


class Plan(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='plan')
    name = models.CharField(max_length=35, help_text='required')
    description = models.TextField(null=True, blank=True, help_text='optional')
    amount_options = models.IntegerField(choices=AMOUNT_CHOICES, default=1)
    tenure_options = models.IntegerField(choices=TENURE_CHOICES, default=1)
    benefit_type = models.IntegerField(choices=BENEFIT_CHOICES, default=1)
    benefit_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'plan'
        app_label = 'brand'
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}.{self.name}'


class Promotion(BaseModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='promotion')
    name = models.CharField(max_length=35, help_text='required')
    code = models.CharField(max_length=10, unique=True)
    promotion_type = models.IntegerField(choices=PROMOTION_CHOICES, default=1)
    redeemable_user = models.IntegerField(default=0)
    valid_from = models.DateField('Promotion Valid From', null=True, blank=True,
                                  help_text='It is required if promotion type is 2')
    valid_to = models.DateField('Promotion Valid To', null=True, blank=True,
                                help_text='It is required if promotion type is 2')
    redeemed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}.{self.name}'

    class Meta:
        db_table = 'promotion'
        app_label = 'brand'
        ordering = ['-id']

    def is_valid(self):
        if not self.is_active:
            return False, 'This Promotion is not available anymore!'

        if self.promotion_type == 1 and self.redeemable_user <= self.redeemed:
            return False, 'User limit has been exhausted for this promotion!'

        if self.promotion_type == 2:
            if self.valid_from < datetime.now() < self.valid_to:
                return False, 'This Promotion has been expired!'

        return True, 'Congratulations, Promotion Applied!'

