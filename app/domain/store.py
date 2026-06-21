"""Seed data used by the dev server's order-placed endpoint.

This mimics a distributor ("Acme Distribution") whose fulfilment team should
receive an email every time one of their retailers places an order.
"""
from app.domain.enums import ContactType
from app.domain.models import Contact, Instance, Order, OrderLine, Organisation


def build_seed_instance() -> Instance:
    return Instance(
        slug='acme',
        name='Acme Distribution',
        contacts=[
            Contact('Ama (Fulfilment Lead)', 'ama@acme-distribution.com', ContactType.FULFILMENT),
            Contact('Kofi (Warehouse)', 'kofi@acme-distribution.com', ContactType.FULFILMENT),
            Contact('Esi (New Hire)', '', ContactType.FULFILMENT),
            Contact('Finance', 'finance@acme-distribution.com', ContactType.FINANCE),
        ],
    )


def build_sample_order(instance: Instance) -> Order:
    return Order(
        id=4071,
        organisation=Organisation(name='Mensah Corner Shop'),
        instance=instance,
        lines=[
            OrderLine(sku='SOAP-12', quantity=3, unit_price=550),
            OrderLine(sku='RICE-5KG', quantity=2, unit_price=1200),
        ],
    )
