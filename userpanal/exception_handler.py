
def log_exception(func):
    def send_mail_on_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            import sys, cgitb
            from pnr_utils import send_Email
            send_Email(
                message=u'{} \n\n {}'.format(e.message, cgitb.html(sys.exc_info())),
                subject='www.trainstatusonline.in Error log_exception!',
                to_addr='niraj.bilaimare@gmail.com'
            )
            raise
    return send_mail_on_exception

