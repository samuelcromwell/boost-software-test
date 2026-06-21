class Config:
    """Base config, mirrors how a Boost instance runs in development."""

    ENV = 'development'
    SECRET_KEY = 'dev-not-secret'
    TESTING = False

    MAIL_DEFAULT_SENDER = 'noreply@boost.technology'
    # Custom backend that mimics our real one: in "internal" environments
    # (development/build/staging) it strips external recipients before sending,
    # so that real customers are never emailed from a non-production system.
    MAIL_BACKEND = 'app.mail.EmailBackend'


class TestConfig(Config):
    """Config used by the test suite.

    Note: the test environment is NOT one of the internal environments, so the
    external-recipient stripping in ``app/mail.py`` does not apply here.
    """

    ENV = 'test'
    TESTING = True
    # Store sent messages in ``mail.outbox`` instead of printing/sending them.
    MAIL_BACKEND = 'locmem'
