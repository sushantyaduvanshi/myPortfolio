from celery import shared_task
import requests
import json
import os
import time

@shared_task
def send_slack(channel, message):
    requests.get(f"{os.getenv('SLACK_URL')}/slack/send", params={
        "channel": channel,
        "message": message
    })
    
@shared_task
def send_visitor_notification():
    for i in range(10):
        print(f"{10-i}...")
        time.sleep(1)
    print("sending slack...")
    with open("visitor.json") as file:
        visitor = json.load(file)
    visitor["total_visit_count"] += 1
    with open("visitor.json","w") as file:
        json.dump(visitor, file, indent=4)
    send_slack(
        "home-server",
        f"You have a visitor. Total visit count : {visitor['total_visit_count']}"
    )