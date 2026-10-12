import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# Initialize a lightweight, local, in-memory vector storage database instance
chroma_client = chromadb.Client()

# CHANGED: Using a completely free, local text embedder that doesn't need an API key
local_ef = embedding_functions.DefaultEmbeddingFunction()

# Create a clean metadata schema collection for historical enterprise customer records
customer_feature_store = chroma_client.create_collection(
    name="customer_historical_profiles", 
    embedding_function=local_ef
)

def populate_historical_feature_store():
    """
    Seeds the local vector database with historical context profiles.
    This acts as the AI's long-term memory layer regarding user attributes.
    """
    print("\n[Vector Database]: Materializing historical profile collection layers...")
    
    # Mock profiles showing historical metrics and churn risks
    customer_ids = ["CUST-992", "CUST-441", "CUST-115"]
    historical_summaries = [
        "Customer Value Tier: VIP Platinum. Lifetime Spend: £4500. Churn Risk Score: 85%. Notes: Package was noted lost by courier service yesterday.",
        "Customer Value Tier: Free Tier. Lifetime Spend: £0. Churn Risk Score: 10%. Notes: Frequently asks general product design preferences.",
        "Customer Value Tier: Standard Enterprise. Lifetime Spend: £1200. Churn Risk Score: 40%. Notes: Experienced an unresolved billing double-charge glitch last month."
    ]
    
    customer_feature_store.add(
        documents=historical_summaries,
        ids=customer_ids
    )
    print("[Vector Database]: Feature layer populate complete.")

def get_customer_context_feature(customer_id: str) -> str:
    """
    Queries the vector database instantly using the customer ID to retrieve 
    historical behavioral context for the AI agent prompt.
    """
    try:
        result = customer_feature_store.get(ids=[customer_id])
        if result and result['documents']:
            return result['documents'][0]
        return "No historical context profile found for this identifier."
    except Exception as e:
        return f"Error retrieving context profile vector: {str(e)}"

# Quick syntax verification execution block
if __name__ == "__main__":
    populate_historical_feature_store()
    test_query = get_customer_context_feature("CUST-992")
    print(f"\n[Test Vector Query Result for CUST-992]:\n{test_query}")
