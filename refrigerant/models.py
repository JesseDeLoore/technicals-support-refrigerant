from django.db import models, DataError, IntegrityError
from django.db.models import F


class Vessel(models.Model):
    name = models.CharField(max_length=100)
    content = (
        models.PositiveIntegerField()
    )  # Amount of refrigerant in the vessel, in kilograms

    @classmethod
    def withdraw(cls, vessel_id: int, amount: int)->int|None:
        """
        Do an atomic update of the vessel content
        Returns 1 if the vessel was updated
        Returns 0 if no row was found to update
        Returns None if there is not enough content in the vessel to withdraw the amount requested.
        """
        try:
            # Once updated to Django>=5 we can leerage the UPDATE ... RETURNING ... syntax to return the amount left in the vessel.
            return cls.objects.filter(id=vessel_id).update(content=F("content") - amount)
        except (DataError, IntegrityError):
            return None

