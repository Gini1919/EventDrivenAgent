import time
import random

def generate_live_customer_stream():
    """
    Simulates a high-latency streaming event queue (e.g., Kafka/Kinesis topic)
    delivering real-time, unstructured customer conversation data.
    """
    mock_tickets = [
        {
            "ticket_id": "TCK-101",
            "customer_id": "CUST-992",
            "message": "Hey! My package hasn't arrived yet. It's been two weeks and your tracker is completely frozen. I want a refund right now or I am canceling my account.",
            "channel": "live_chat"
        },
        {
            "ticket_id": "TCK-102",
            "customer_id": "CUST-441",
            "message": "Hi there, I just wanted to ask if you support dark mode on the mobile app? The current UI is a bit too bright for me at night.",
            "channel": "mobile_app"
        },
        {
            "ticket_id": "TCK-103",
            "customer_id": "CUST-115",
            "message": "URGENT: I see an unauthorized charge of £120 on my statement from your company today. Secure my account immediately, this is completely unacceptable!",
            "channel": "web_portal"
        }
    ]
    
    print("[Streaming Source]: Activating real-time event ingestion line...")
    for ticket in mock_tickets:
        # Simulate real-time streaming intervals
        time.sleep(1)
        yield ticket

if __name__ == "__main__":
    # Test execution block to verify the ingestion loop runs cleanly
    for event in generate_live_customer_stream():
        print(f"\n[Ingested Event Log] ID: {event['ticket_id']} | Source: {event['channel']}")
        print(f"Message: {event['message']}")
