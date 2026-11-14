# XX Global Telemetry Engine

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/status-learning%20project-lightgrey)

A telemetry ingestion and validation pipeline inspired by Site Reliability Engineering (SRE) data governance practices. The engine reads incoming event logs, fills in missing metadata, flags service-level agreement (SLA) latency breaches, and isolates corrupted payloads so that one bad record never halts a live run.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Sample Output](#sample-output)
- [Key Engineering Takeaways](#key-engineering-takeaways)

## Overview

Telemetry streams are rarely clean. Records arrive with missing fields, impossible values, or no payload at all. This project demonstrates a defensive approach to handling that reality:

- **Metadata enrichment:** records with no region are tagged `unassigned-edge` instead of being dropped.
- **Structural validation:** every record must carry a `request_id`, a `payload`, and a non-negative latency value.
- **SLA auditing:** any response time above `100.0ms` is flagged as a critical violation.
- **Fault isolation:** invalid records are routed to a Dead Letter Queue (DLQ) so the pipeline keeps running.

## System Architecture

```text
[ High-Volume Event Stream (telemetry_bench.py) ]
                       │
                       ▼
[ Ingestion Logic Shield (ingest_shield.py) ]
  ├── 1. Metadata Enrichment  ──► Injects "unassigned-edge" if region is missing
  ├── 2. Structural Integrity ──► Validates request_id, payload, and non-negative latency
  └── 3. SLA Latency Auditor  ──► Flags response times exceeding 100.0ms
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
[ Production Vault ]          [ Dead Letter Queue ]
(Valid Event Records)         (Corrupted Payloads)
        │
        ▼
[ Automated Reporting (metrics_manifest.txt) ]
```

## Project Structure

| File | Purpose |
| --- | --- |
| `ingest_shield.py` | Core `process_telemetry_stream` engine. Uses defensive dictionary lookups (`.get()`) to avoid runtime crashes, updates missing regional fields in place, and sorts records into validation buckets. |
| `telemetry_bench.py` | Simulates an inbound API stream with valid logs, missing regional tags, SLA latency spikes, and corrupted records. Feeds the batch to the ingestion shield and writes the run summary to disk. |
| `metrics_manifest.txt` | Auto-generated report covering total events processed, clean vault ingestions, DLQ isolations, and critical SLA violations. |

## Getting Started

**Prerequisites:** Python 3 installed and available from your terminal.

1. Navigate into the project directory:

   ```cmd
   cd XX_telemetry
   ```

2. Run the stream generator benchmark:

   ```cmd
   py telemetry_bench.py
   ```

3. View the generated health report:

   ```cmd
   type metrics_manifest.txt
   ```

## Sample Output

Contents of `metrics_manifest.txt` after a run:

```text
GOOGLE METRICS RUN MANIFEST REPORT

Total Stream Events Evaluated: 5
Clean Vault Records Ingested: 3
Corrupted Records Isolated in DLQ: 2
Critical SRE Latency SLA Violations: 1
```

## Key Engineering Takeaways

- **Defensive state mutation:** Missing metadata should be filled in place (`log_record["region"] = "unassigned-edge"`) before a record is appended to any downstream vault.
- **Loop scope control:** The summary block must sit outside the main iteration loop, otherwise the function exits after the first record.
- **Automated observability:** Production pipelines run unattended, so they need automated threshold alerts (such as latency above `100.0ms`) and persistent manifest logs for auditing.
