from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from brand.models import Plan
from apps.custom_fields import AMOUNT_CHOICES, TENURE_CHOICES, BENEFIT_CHOICES
from apps.default import BaseModel
from django.db import models


class CustomerGoal(BaseModel):
    """
        Customer Goal Model
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='goals')
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    selected_amount = models.IntegerField(choices=AMOUNT_CHOICES, default=1)
    selected_tenure = models.IntegerField(choices=TENURE_CHOICES, default=1)
    benefit_type = models.IntegerField(choices=BENEFIT_CHOICES, default=1)
    benefit_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    start_date = models.DateTimeField(blank=True, null=True)
    deposit_amount = models.IntegerField(default=0, validators=[MaxValueValidator(1000000), MinValueValidator(0)])
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}. {self.user.username}...{self.plan.name}'

    class Meta:
        db_table = 'customer_goals'
        app_label = 'customer'

    def __init__(self, *args, **kwargs):
        super(CustomerGoal, self).__init__(*args, **kwargs)
        self.__pre_is_active = self.is_active

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if not self.__pre_is_active and self.is_active:
            self.start_date = datetime.now()
            self.end_date = self.start_date + timedelta(days=28*self.selected_tenure)
        super(CustomerGoal, self).save(force_insert, force_update, *args, **kwargs)
