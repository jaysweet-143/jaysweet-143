# Import the validation logic from the ingest_shield.py file
from ingest_shield import process_telemetry_stream

# The main execution test bench engine
if __name__ == "__main__":
    
    # Mocking a high-frequency live stream containing structure, regional, and latency variations
    mock_google_stream = [
        {
            "request_id": "REQ-001",
            "region": "africa-south1",
            "latency_ms": 45.2,
            "payload": {"service": "auth", "status": 200}
        },
        {
            "request_id": "REQ-002",
            "region": None,  # Triggering the unassigned-edge layout logic
            "latency_ms": 12.8,
            "payload": {"service": "billing", "status": 200}
        },
        {
            "request_id": "REQ-003",
            "region": "europe-west1",
            "latency_ms": 320.5,  # Triggering the nested SLA Warning Monitor
            "payload": {"service": "search", "status": 500}
        },
        {
            "request_id": None,  # Triggering the structural logic shield
            "region": "us-central1",
            "latency_ms": 15.0,
            "payload": {"service": "analytics"}
        },
        {
            "request_id": "REQ-005",
            "region": "asia-east1",
            "latency_ms": -5.0,  # Triggering the negative latency validation filter
            "payload": {"service": "maps"}
        }
    ]
    
    print("Launching 'XX' Telemetry Stream Generator Bench...")
    
    # Fire the logs stream into the ingestion engine
    report = process_telemetry_stream(mock_google_stream)
    
    print("STREAM PROCESSING LIFECYCLE COMPLETE.")
    
    # Write the raw outputs directly into  clean metrics text file
    with open("metrics_manifest.txt", "w") as file_writer:
        file_writer.write("'XX' METRICS RUN MANIFEST REPORT\n")
        file_writer.write("----------------------------------\n")
        file_writer.write(f"Total Stream Events Evaluated: {report['total_processed']}\n")
        file_writer.write(f"Clean Vault Records Ingested: {len(report['production_vault'])}\n")
        file_writer.write(f"Corrupted Records Isolated in DLQ: {len(report['dead_letter_queue'])}\n")
        file_writer.write(f"Critical SRE Latency SLA Violations: {report['sla_violations']}\n")
        
    print("Telemetry manifest logs securely written to metrics_manifest.txt")
