from datetime import datetime
from pydantic import BaseModel, Field


class AutoDates(BaseModel):
    created_at: datetime = Field(None, description="Item updated at.")
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Item updated at."
    )

    async def before_update(self):
        self.updated_at = datetime.now()
