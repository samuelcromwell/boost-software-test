import pytest

from app import create_app
from app.config import TestConfig
from app.domain.enums import ContactType
from app.domain.models import Contact, Instance, Order, OrderLine, Organisation


@pytest.fixture
def app():
    flask_app = create_app(TestConfig)
    with flask_app.app_context():
        yield flask_app


@pytest.fixture
def outbox(app):
    """Reset and return the in-memory email outbox for each test.

    With the locmem backend, flask-mailman appends every sent message to an
    ``outbox`` list on the mail extension state.
    """
    state = app.extensions['mailman']
    state.outbox = []
    return state.outbox


@pytest.fixture
def make_instance():
    def _make_instance(fulfilment_emails):
        return Instance(
            slug='acme',
            name='Acme Distribution',
            contacts=[
                Contact(f'Contact {i}', email, ContactType.FULFILMENT)
                for i, email in enumerate(fulfilment_emails)
            ],
        )
    return _make_instance


@pytest.fixture
def make_order(make_instance):
    def _make_order(fulfilment_emails):
        instance = make_instance(fulfilment_emails)
        return Order(
            id=4071,
            organisation=Organisation(name='Mensah Corner Shop'),
            instance=instance,
            lines=[OrderLine(sku='SOAP-12', quantity=3, unit_price=550)],
        )
    return _make_order
