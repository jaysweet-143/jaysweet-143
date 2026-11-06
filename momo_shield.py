def filter_momo_batch(payload_batch):
    # Gate 1: Check if the inbound payload batch list has zero items
    if len(payload_batch) == 0:
        return "CRITICAL_ALERT: EMPTY_PAYLOAD"

    # Create our destination storage vault buckets
    ingested_vault = []
    dead_letter_queue = []
 
    # Look at each individual transaction record dictionary
    for record in payload_batch:
        # Use our safe .get() method to unpack values without app crashes
        sender = record.get("sender_id")
        receiver = record.get("receiver_id")  # Fixed Key name to match test bench
        amount = record.get("amount")
        network = record.get("network")
    
        # Our logical conditions (Kept INSIDE the loop block via indentation)
        is_structurally_sound = (sender is not None) and (receiver is not None)
        is_within_limit = (amount is not None) and (amount > 0 and amount <= 5000)
        is_valid_network = (network == "MTN") or (network == "Telecel")
    
        # Routing decision engine (Kept INSIDE the loop block via indentation)
        if is_structurally_sound and is_within_limit and is_valid_network:
            ingested_vault.append(record)
        else:
            dead_letter_queue.append(record)
    
    # Wrap both destination vault lists inside an output dictionary capsule
    # (Shifted left to sit OUTSIDE the loop, running only after iteration completes)
    return {
         "ingested_vault": ingested_vault,
         "dead_letter_queue": dead_letter_queue
    }
    
# The main execution engine block (Completely outside the function layout)
if __name__ == "__main__": 
    raw_inbound_stream = [
        {"sender_id": "ACC_01", "receiver_id": "ACC_02", "amount": 1200, "network": "MTN"},     # Should Pass
        {"sender_id": "ACC_03", "receiver_id": "ACC_04", "amount": -50,  "network": "Telecel"}, # Fails Amount
        {"sender_id": "ACC_05", "receiver_id": None,     "amount": 2500, "network": "MTN"},     # Fails Structure
        {"sender_id": "ACC_06", "receiver_id": "ACC_07", "amount": 6000, "network": "Telecel"}, # Fails Limit Cap
        {"sender_id": "ACC_08", "receiver_id": "ACC_09", "amount": 450,  "network": "AirtelTigo"} # Fails Network
    ]

    # Trigger the processing lifecycle with matching variable names
    pipeline_result = filter_momo_batch(raw_inbound_stream)

    # Print out our system telemetry
    print("PIPELINE ROUTING OPERATION COMPLETE:")
    print(f"Clean Vault Records Ingested: {len(pipeline_result['ingested_vault'])}")
    print(f"Dirty Records Isolated in DLQ: {len(pipeline_result['dead_letter_queue'])}")
