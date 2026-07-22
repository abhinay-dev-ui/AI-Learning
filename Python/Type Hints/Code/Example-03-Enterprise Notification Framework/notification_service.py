from notification import NotificationProvider

from providers import (
    EmailProvider,
    SMSProvider,
)


class NotificationService:

    def __init__(
        self,
        provider_type: str,
    ) -> None:

        if provider_type == "email":
            self.provider: NotificationProvider = EmailProvider()

        elif provider_type == "sms":
            self.provider = SMSProvider()

        else:
            raise ValueError("Unsupported provider.")

    def notify(
        self,
        recipient: str,
        message: str,
    ) -> None:

        self.provider.send(
            recipient,
            message,
        )