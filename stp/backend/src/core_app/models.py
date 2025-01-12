import uuid

from django.db.models import DateTimeField, Model, UUIDField
from django.utils import timezone


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(db_index=True, default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
