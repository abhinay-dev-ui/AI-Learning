from typing import Protocol


class NotificationProvider(Protocol):

    def send(
        self,
        recipient: str,
        message: str,
    ) -> None:
        ...