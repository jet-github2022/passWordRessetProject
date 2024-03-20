from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailAccountActivation(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


email_account_activation = EmailAccountActivation()

