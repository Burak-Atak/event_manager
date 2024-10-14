from enumfields import Enum


class NotificationTypeEnum(Enum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'

    class Labels:
        EMAIL = 'Email'
        SMS = 'SMS'
        PUSH = 'Push'


class NotificationStatus(Enum):
    SENT = 'sent'
    FAILED = 'failed'

    class Labels:
        SENT = 'Sent'
        FAILED = 'Failed'

    def to_json(self):
        return {'status': self.status}