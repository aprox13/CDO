class Alert:
    # Bootstrap alert class
    TYPE_SUCCESS = 'alert-success'
    TYPE_PRIMARY = 'alert-primary'
    TYPE_DANGER = 'alert-danger'
    ALERT_TAG = 'ALERT_TAG'

    type = TYPE_SUCCESS
    title = 'Success'
    message = ''

    def __init__(self, alert_type=TYPE_SUCCESS, alert_title='Success', alert_message=''):
        self.type = alert_type
        self.title = alert_title
        self.message = alert_message

    def __str__(self):
        return 'Alert<' + self.type + ', ' + self.title + ', ' + self.message + '>'

