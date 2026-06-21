"""Custom email backend.

This mirrors a real safeguard in the Boost platform: in non-production
("internal") environments we must never email real customers, so external
recipients are stripped from every message before it is sent. Only addresses
on an internal domain are kept.

In development the underlying backend simply prints messages to the console.
"""
from email.utils import parseaddr

from flask import current_app
from flask_mailman.backends.console import EmailBackend as ConsoleBackend

INTERNAL_EMAIL_DOMAINS = ('boost.technology',)
EMAIL_INTERNAL_ENVIRONMENTS = ('build', 'staging')


def _address_domain(address):
    email_address = parseaddr(address)[1].strip().lower()
    if '@' not in email_address:
        return None
    return email_address.rsplit('@', maxsplit=1)[1]


class EmailBackend(ConsoleBackend):
    def send_messages(self, email_messages):
        if current_app.config['ENV'] in EMAIL_INTERNAL_ENVIRONMENTS:
            email_messages = self._strip_external_recipients(email_messages)

        return super().send_messages(email_messages)

    def _strip_external_recipients(self, email_messages):
        kept_messages = []
        for message in email_messages:
            internal = [
                address for address in message.to
                if _address_domain(address) in INTERNAL_EMAIL_DOMAINS
            ]
            removed = [address for address in message.to if address not in internal]

            if removed:
                current_app.logger.warning(
                    'Removed external recipients in protected environment: %s',
                    ', '.join(removed),
                )

            message.to = internal
            if message.to:
                kept_messages.append(message)
            else:
                current_app.logger.warning(
                    'No remaining internal recipients in protected environment',
                )

        return kept_messages
