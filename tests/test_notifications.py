from app.adapters import notifications


def test_notify_email_sends_to_a_single_address(app, outbox):
    result = notifications.notify_email(
        to_addresses='ama@acme-distribution.com',
        subject='Order placed',
        body='<p>An order was placed.</p>',
    )

    assert result == 1
    assert len(outbox) == 1
    assert outbox[0].to == ['ama@acme-distribution.com']
    assert outbox[0].subject == 'Order placed'


def test_notify_email_sends_to_multiple_addresses(app, outbox):
    result = notifications.notify_email(
        to_addresses=['ama@acme-distribution.com', 'kofi@acme-distribution.com'],
        subject='Order placed',
        body='<p>An order was placed.</p>',
    )

    assert result == 1
    assert len(outbox) == 1
    assert outbox[0].to == ['ama@acme-distribution.com', 'kofi@acme-distribution.com']


def test_notify_email_order_placed_emails_the_fulfilment_team(app, outbox, make_order):
    order = make_order([
        'ama@acme-distribution.com',
        'kofi@acme-distribution.com',
    ])

    notifications.notify_email_order_placed(order)

    assert len(outbox) == 1
    assert outbox[0].to == [
        'ama@acme-distribution.com',
        'kofi@acme-distribution.com',
    ]
    assert outbox[0].subject == 'Boost: Order placed'
    assert 'Mensah Corner Shop' in outbox[0].body


def test_notify_email_order_placed_ignores_blank_fulfilment_emails(app, outbox, make_order):
    order = make_order([
        'ama@acme-distribution.com',
        '',
        'kofi@acme-distribution.com',
    ])

    result = notifications.notify_email_order_placed(order)

    assert result == 1
    assert len(outbox) == 1
    assert outbox[0].to == [
        'ama@acme-distribution.com',
        'kofi@acme-distribution.com',
    ]


def test_notify_email_order_placed_with_no_fulfilment_contacts(app, outbox, make_order):
    order = make_order([])

    result = notifications.notify_email_order_placed(order)

    assert result is None
    assert outbox == []
