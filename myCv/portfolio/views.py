from django.views.generic import TemplateView
import requests
import json
import os

# Create your views here.

class index(TemplateView):
    template_name = 'index.html'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        with open("visitor.json") as file:
            visitor = json.load(file)
        visitor["total_visit_count"] += 1
        requests.get(f"{os.getenv('SLACK_URL')}/slack/send", params={
            "channel": "home-server",
            "message": f"You have a visitor. Total visit count : {visitor['total_visit_count']}"
        })
        with open("visitor.json","w") as file:
            json.dump(visitor, file, indent=4)