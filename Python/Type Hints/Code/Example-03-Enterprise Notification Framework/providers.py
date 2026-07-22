class EmailProvider:

    def send(
        self,
        recipient: str,
        message: str,
    ) -> None:

        print(
            f"[Email] Sending email to {recipient}: {message}"
        )


class SMSProvider:

    def send(
        self,
        recipient: str,
        message: str,
    ) -> None:

        print(
            f"[SMS] Sending SMS to {recipient}: {message}"
        )