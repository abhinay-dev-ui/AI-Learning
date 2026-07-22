from notification_service import NotificationService


def main() -> None:

    email_service = NotificationService(
        "email"
    )

    email_service.notify(
        "john@example.com",
        "Welcome to the company!",
    )

    print()

    sms_service = NotificationService(
        "sms"
    )

    sms_service.notify(
        "+91 9876543210",
        "Your salary has been credited.",
    )


if __name__ == "__main__":
    main()