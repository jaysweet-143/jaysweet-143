# ==============================================================================
# PROJECT: Automated Inbound Transaction Router Engine
# SKILL DISCIPLINE: Programmatic Thinking, Boolean Logic & Data Validation
# SYSTEM ARCHITECTURE: Edge Logic Shield / Dead Letter Queue (DLQ) Router
# ==============================================================================

def execute_data_router_lifecycle(transaction_payload):
    """
    Evaluates incoming record integrity using conditional structures,
    boolean comparison states, and custom logic safeguards.
    """
    print("Initializing logic shield lifecycle...")
    print("--------------------------------------------------")
    
    # Trackers for system execution states
    clean_ingested_vault = []
    dead_letter_queue = []
    
    # 1. Primary Conditional Check: Is the batch totally empty?
    if len(transaction_payload) == 0:
        print("SYSTEM ALERT [CRITICAL]: Zero data rows received. Aborting.")
        return "ROUTING_FAILED: EMPTY_BATCH"
    
    # 2. Iterate through incoming data packets step-by-step
    for index, record in enumerate(transaction_payload):
        print(f"Auditing Record ID {index + 1}...")
        
        # Extract variables using a safe fallback to prevent structural crashes
        tx_id = record.get("transaction_id")
        amount = record.get("amount")
        currency = record.get("currency")
        
        # 3. Apply Strict Boolean and Comparison Logic Gates
        # Rule A: Transaction ID must exist (Is Not None)
        # Rule B: Amount must be a positive number (> 0)
        # Rule C: Currency flag must be supported (e.g., GHS, USD)
        
        is_structurally_sound = (tx_id is not None)
        has_positive_value = (amount is not None and amount > 0)
        is_supported_currency = (currency == "GHS" or currency == "USD")
        
        # 4. Final Routing Decision Matrix (If-Else Structure)
        if is_structurally_sound and has_positive_value and is_supported_currency:
            print(f" -> SUCCESS: Record {tx_id} passed validation gates.")
            clean_ingested_vault.append(record)
        else:
            print(f" -> WARNING: Data anomaly detected on Record index {index + 1}. Routing to Dead Letter Queue.")
            dead_letter_queue.append({
                "raw_record": record,
                "failure_reason": f"Integrity Failure (Sound={is_structurally_sound}, Positive={has_positive_value}, Currency={is_supported_currency})"
            })
            
    print("--------------------------------------------------")
    print("EXECUTION SUMMARY:")
    print(f"Vault Ingestion Rows: {len(clean_ingested_vault)}")
    print(f"Dead Letter Queue Isolation Rows: {len(dead_letter_queue)}")
    
    return "ROUTING_COMPLETE"


# ==============================================================================
# SYSTEM TEST BENCH (Simulating messy real-world inbound API payloads)
# ==============================================================================
if __name__ == "__main__":
    
    # Mocking a live financial data stream coming from an upstream API
    mock_inbound_stream = [
        {"transaction_id": "TXN_1001", "amount": 1500.50, "currency": "GHS"}, # Valid row
        {"transaction_id": "TXN_1002", "amount": -200.00, "currency": "USD"}, # Invalid (Negative value)
        {"transaction_id": None,       "amount": 5000.00, "currency": "GHS"}, # Invalid (Missing ID)
        {"transaction_id": "TXN_1004", "amount": 450.00,  "currency": "EUR"}  # Invalid (Unsupported currency)
    ]
    
    # Execute the engineering automation model
    status = execute_data_router_lifecycle(mock_inbound_stream)
    print(f"Final Pipeline System Code: {status}")
