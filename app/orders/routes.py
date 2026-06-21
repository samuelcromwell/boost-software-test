from flask import Blueprint, current_app, jsonify

from app.adapters import notifications
from app.domain.store import build_sample_order, build_seed_instance

bp = Blueprint('orders', __name__)


@bp.post('/orders/place-sample')
def place_sample_order():
    """Place a sample order and notify the fulfilment team.

    This exists so you can exercise the order-placed email flow end to end
    against the seed data (see app/domain/store.py). Watch the server logs.
    """
    instance = build_seed_instance()
    order = build_sample_order(instance)

    current_app.logger.info(
        'Order #%s placed for %s — notifying the fulfilment team',
        order.id,
        order.organisation.name,
    )
    notifications.notify_email_order_placed(order)

    return jsonify({
        'order_id': order.id,
        'organisation': order.organisation.name,
    })
