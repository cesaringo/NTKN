from datetime import date, datetime
from django.db import models
from authentication.models import Account
from localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import Group
from slugify import slugify
from ntkn import settings



