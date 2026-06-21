from flask import current_app, render_template
from flask_mailman import EmailMessage

from app.domain.enums import ContactType


def notify_email(to_addresses, subject, body, fail_silently=False):
    if not isinstance(to_addresses, list):
        to_addresses = [to_addresses]

    if any(not address for address in to_addresses):
        return False

    message = EmailMessage(
        subject,
        body,
        from_email=current_app.config['MAIL_DEFAULT_SENDER'],
        to=to_addresses,
    )
    message.content_subtype = 'html'

    return message.send(fail_silently=fail_silently)


def notify_email_order_placed(order):
    """Email the instance's fulfilment contacts when an order is placed."""
    to_addresses = [
        contact.email
        for contact in order.instance.contacts_for(ContactType.FULFILMENT)
    ]
    if not to_addresses:
        return None

    html = render_template(
        'email/notifications.html',
        title='Order placed',
        preheader=f'{order.organisation.name} placed an order',
        heading=f'{order.organisation.name} placed an order',
        content=(
            f'{len(order.lines)} item(s) for {order.display_total} requires fulfilment.'
        ),
        cta_label='View order',
        cta_url=f'https://app.boost.technology/orders/{order.id}',
    )

    return notify_email(
        to_addresses=to_addresses,
        subject='Boost: Order placed',
        body=html,
    )
