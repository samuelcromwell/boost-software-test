Acme Distribution has three fulfilment contacts in the customer data, but the new hire, Esi, has a blank email address. The same setup is mirrored in the app seed data used by `/orders/place-sample`.

When an order is placed, `notify_email_order_placed()` collects every fulfilment contact email, including blank ones, and passes the full list into `notify_email()`. `notify_email()` refuses to send if any address in the list is empty, so the recipient list `['ama@acme-distribution.com', 'kofi@acme-distribution.com', '']` causes the whole notification to be dropped.

That is why orders are still being created successfully, but nobody on the fulfilment team receives the email after the incomplete new contact was added.
