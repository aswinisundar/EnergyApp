from django.db import models
from django.contrib.auth.models import User


class energyMonthlyUsage:
    def __init__(self,day,usage):
        self.day = day
        self.dayOfMonth=day.day
        self.month=day.month
        self.usage = usage



