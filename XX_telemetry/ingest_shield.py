def process_telemetry_stream(stream_batch):
    # If the incoming telemetry batch has zero events, abort immediately
    if len(stream_batch) == 0:
        return "METRIC_ALERT: EMPTY_STREAM_STREAM"

    # Production Vault Storage Buckets
    production_vault = []
    dead_letter_queue = []
    
    # Telemetry Monitoring Metrics (Tracked for SRE health reports)
    total_processed = 0
    sla_violations_count = 0    

    # Iterate through the continuous high-volume telemetry stream
    for log_record in stream_batch:
        total_processed += 1
        
        # Use the safe .get() method to prevent unexpected schema crashes
        request_id = log_record.get("request_id")
        region = log_record.get("region")
        latency = log_record.get("latency_ms")  # Match standard test key
        payload = log_record.get("payload")

        if region is None:
            region = "unassigned-edge"
            log_record["region"] = region

        # Validation Logic Shields
        is_structurally_sound = (request_id is not None) and (payload is not None)

        # Performance Check: Evaluate latency microsecond thresholds
        is_latency_valid = (latency is not None) and (latency >= 0)

        # 1. Main Data Integrity Gateway
        if is_structurally_sound and is_latency_valid:
            production_vault.append(log_record) 
   
            # 2. Nested SLA Monitor Check: Flag slow response times
            if latency > 100.0:
                sla_violations_count += 1
                print(f"SRE MONITOR [WARNING]: SLA violation on {request_id}. Latency: {latency}ms")
        else:
            dead_letter_queue.append(log_record)
    
    # This guarantees the report generates only AFTER every single log has been processed.
    return {
        "production_vault": production_vault,
        "dead_letter_queue": dead_letter_queue,
        "total_processed": total_processed,
        "sla_violations": sla_violations_count
    }
