from pydantic import BaseModel, Field, field_validator


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty")
        return cleaned
