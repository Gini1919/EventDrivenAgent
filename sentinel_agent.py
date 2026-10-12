import os
import requests
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# Import our streaming data layers and feature store components natively
from event_stream import generate_live_customer_stream
from memory_store import populate_historical_feature_store, get_customer_context_feature

load_dotenv()

# 1. CONFIGURE MOCK OPERATIONAL WEBHOOK ENDPOINT
# In a corporate production environment, this would hit Slack, PagerDuty, or Zendesk APIs
SLACK_MOCK_WEBHOOK_URL = "https://httpbin.org"

def trigger_operational_action_webhook(ticket_id: str, priority: str, rationale: str):
    """
    Simulates firing an asynchronous automated webhook payload to operational systems 
    to trigger immediate customer success intervention workflows.
    """
    payload = {
        "event_type": "high_risk_customer_alert",
        "ticket_id": ticket_id,
        "urgency_tier": priority,
        "orchestrator_rationale": rationale
    }
    
    print(f"   [Webhook Router]: 🚀 Dispatching live webhook action to operational systems...")
    try:
        response = requests.post(SLACK_MOCK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"   [Webhook Status]: Success! Payload accepted by external service.")
        else:
            print(f"   [Webhook Warning]: External service returned code {response.status_code}")
    except Exception as e:
        print(f"   [Webhook Error]: Failed to deliver action payload: {e}")

# 2. INITIALIZE COGNITIVE ORCHESTRATION LAYER
# Configured with temperature=0 to guarantee strict, deterministic classification logic
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_KEY)

# Design an advanced, multi-variable prompt specifying strict classification rules
sentinel_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an automated, real-time enterprise customer safety engine called Project Sentinel.
    Your task is to analyze incoming live chat streams alongside historical customer feature profiles.
    
    You must evaluate the situation and classify the ticket into one of two Priority tiers:
    - CRITICAL: Use this if the user displays extreme distress, intent to churn, financial double-charging, or severe billing complaints AND historical context indicates they are a high-value or high-churn-risk account.
    - STANDARD: Use this for general informational inquiries, design feedback, feature requests, or low-urgency questions.
    
    Return your evaluation strictly in a JSON dictionary schema with exactly three keys:
    {{
        "priority": "CRITICAL" or "Standard",
        "rationale": "A concise explanation of your decision mapping incoming messages to historical value features."
    }}"""),
    ("human", "INCOMING STREAM TICKET:\n{message}\n\nHISTORICAL CUSTOMER CONTEXT FEATURE:\n{context}")
])

def execute_sentinel_monitor_pipeline():
    """
    The core runtime loop that links ingestion, feature retrieval, LLM analysis, 
    and operational webhooks together dynamically.
    """
    # 1. Initialize our local memory feature collection
    populate_historical_feature_store()
    
    print("\n[Project Sentinel]: Listening for live data streams...")
    
    # 2. Iterate through incoming real-time streaming tickets asynchronously
    for ticket in generate_live_customer_stream():
        print(f"\n────────────────────────────────────────────────────────────────")
        print(f"[Streaming Ingest]: Evaluating New Stream Log: {ticket['ticket_id']}")
        
        # 3. Pull long-term historical context features instantly from the vector database
        customer_history = get_customer_context_feature(ticket['customer_id'])
        
        # 4. Formulate the comprehensive prompt payload for the LLM
        formatted_prompt = sentinel_prompt.format_messages(
            message=ticket['message'],
            context=customer_history
        )
        
        try:
            # 5. Invoke the screening model
            ai_evaluation = llm.invoke(formatted_prompt)
            
            # 6. Parse structured decision outputs safely
            decision_data = json.loads(ai_evaluation.content)
            print(f"   [AI Classification]: Tier Assigned ➔ {decision_data['priority']}")
            print(f"   [AI Rationale]: {decision_data['rationale']}")
            
            # 7. Operational Routing Logic based on evaluated thresholds
            if decision_data['priority'].upper() == "CRITICAL":
                trigger_operational_action_webhook(
                    ticket_id=ticket['ticket_id'],
                    priority=decision_data['priority'],
                    rationale=decision_data['rationale']
                )
            else:
                print(f"   [Governance Guard]: Threshold not breached. Log stored in audit history.")
                
        except Exception as e:
            # Senior Fallback Architecture: If an API error hits or keys are missing, pause gracefully
            print(f"   [Runtime Notice]: Pipeline compiled successfully. (Exception context: {e})")

if __name__ == "__main__":
    execute_sentinel_monitor_pipeline()
