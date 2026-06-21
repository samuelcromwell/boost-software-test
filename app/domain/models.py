"""A deliberately tiny, in-memory domain.

In the real Boost platform these are SQLAlchemy/Mongo models backed by
PostgreSQL. For this test they are plain dataclasses so the project runs
anywhere with no database to set up.
"""
from dataclasses import dataclass, field

from app.domain.enums import ContactType


@dataclass
class Organisation:
    name: str


@dataclass
class Contact:
    name: str
    email: str
    type: ContactType


@dataclass
class Instance:
    """A tenant (one of our distributors / suppliers)."""

    slug: str
    name: str
    contacts: list[Contact] = field(default_factory=list)

    def contacts_for(self, contact_type: ContactType) -> list[Contact]:
        return [contact for contact in self.contacts if contact.type == contact_type]


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price: int  # minor units (e.g. cents)


@dataclass
class Order:
    id: int
    organisation: Organisation
    instance: Instance
    lines: list[OrderLine] = field(default_factory=list)
    currency: str = 'USD'

    @property
    def total(self) -> int:
        return sum(line.quantity * line.unit_price for line in self.lines)

    @property
    def display_total(self) -> str:
        return f'{self.currency} {self.total / 100:,.2f}'
