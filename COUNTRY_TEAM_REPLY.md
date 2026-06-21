Hi Michael,

Thanks for flagging this. I checked Acme Distribution's fulfilment contact setup and found that the newly added fulfilment user does not have an email address saved yet. Our order-email logic was treating that blank address as a hard failure, which stopped the notification from being sent to the rest of the fulfilment team as well.

I've fixed the issue so blank fulfilment email fields are ignored and valid contacts like Ama and Kofi still receive order emails. It would still be worth completing the new team member's profile so they can start receiving the same notifications too.

Thanks,
