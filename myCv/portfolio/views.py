from django.views.generic import TemplateView
from portfolio.tasks import send_visitor_notification

# Create your views here.

class index(TemplateView):
    template_name = 'index.html'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        send_visitor_notification.delay()