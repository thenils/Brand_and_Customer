from django.utils.translation import gettext_lazy as _


def get_default_address():
    """
        Get default address format for JSONField
    """
    return {
        'street': '',
        'city': '',
        'state': '',
        'pin_code': '',
        'country': ''
    }


AMOUNT_OPTIONS = [1, 2, 3, 4, 5, 6]
AMOUNT_CHOICES = (
    (1, 9),
    (2, 19),
    (3, 29),
    (4, 39),
    (5, 49),
    (6, 59),
)

TENURE_OPTIONS = [1, 2, 3, 4, 5, 6]
TENURE_CHOICES = (
    (1, 1),
    (2, 3),
    (3, 6),
    (4, 9),
    (5, 12),
    (6, 18),
)

BENEFIT_OPTIONS = [1, 2, 3]
BENEFIT_CHOICES = (
    (1, _("CASHBACK")),
    (2, _("EXTRA_CASHBACK")),
    (3, _("WALLET_POINT")),
)

PROMOTION_OPTIONS = [1, 2]
PROMOTION_CHOICES = (
    (1, _("BY NUMBER OF USER")),
    (2, _("BY TIME PERIOD")),
)
