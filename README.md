# ELK Stack Home Lab — Local Deployment on Linux Mint

## Overview
Deployed a full Elastic Stack (Elasticsearch, Logstash, Kibana, Filebeat) 
locally on Linux Mint to gain hands-on experience with log ingestion, 
indexing, and visualization. This lab simulates a real SIEM environment 
and was used to explore Elasticsearch APIs and Kibana dashboards.

## Stack
- Elasticsearch 8.19.14 — search and analytics engine / data store
- Kibana 8.19.14 — visualization and dashboard layer
- Logstash — log processing pipeline
- Filebeat 8.19.14 — lightweight log shipper (system module enabled)

## What I Did
- Installed and configured all four Elastic Stack components from scratch
  on Linux Mint 22.1 using apt
- Diagnosed and resolved three real-world issues during setup:
  - Stale apt cache preventing Elasticsearch installation
  - Filebeat crashing due to misconfigured module filesets
  - Kibana losing Elasticsearch connectivity after network change
- Resolved OOM kill of Elasticsearch by tuning JVM heap size
- Configured Filebeat to ship system logs into Elasticsearch over HTTPS
- Verified data ingestion using Kibana Discover with 19,000+ live events

## Elasticsearch API Queries Used
- `GET /` — cluster identity and version info
- `GET /_cluster/health` — cluster health status
- `GET /_cat/indices?v` — list all indices with size and doc count
- `GET /_nodes?pretty` — node configuration and stats
- `GET /_cluster/settings?pretty` — cluster-wide settings

## SIEM Dashboard — SSH Login Monitor

Built a security monitoring dashboard in Kibana that visualizes SSH authentication events in real time.
<img width="1919" height="960" alt="Complete_dashboard" src="https://github.com/user-attachments/assets/47de6ee0-ebc9-4541-948e-73a2f434aabb" />
<img width="1909" height="707" alt="Attack Map" src="https://github.com/user-attachments/assets/ba058aff-f902-42ef-bd42-e7696edb7a20" />

## Logstash Enrichment Pipeline

Built a Logstash pipeline that intercepts raw auth logs from Filebeat, enriches them, and routes them to a dedicated security index.

### Data Flow

Filebeat → Logstash (port 5044) → Filter/Enrich → Elasticsearch → Kibana

### What the Pipeline Does
- Classifies events using pattern matching on raw message content
- Tags failed logins with `ssh_failed_login` and `brute_force_attempt`
- Tags successful logins with `ssh_successful_login`
- Tags invalid user attempts with `ssh_invalid_user`
- Adds structured `event_type` field for clean querying
- Extracts source IP using Grok pattern matching
- Enriches external IPs with GeoIP city, country, and coordinates
- Routes enriched events to a daily index `logstash-ssh-YYYY.MM.dd`

<img width="1919" height="1040" alt="Enriched Data" src="https://github.com/user-attachments/assets/d8ba6893-2ca8-4794-95fb-2e3796411d68" />

---

## Attack Simulation

Used Hydra to simulate SSH brute force attacks to generate realistic authentication data for dashboard testing. Maps to MITRE ATT&CK technique **T1110.001 — Brute Force: Password Guessing**.
## Troubleshooting Log
### Issue 1 — Unable to locate package elasticsearch
**Cause:** apt package cache was stale after adding the Elastic repo.
**Fix:** Re-ran `sudo apt update` and confirmed it pulled from artifacts.elastic.co before installing.

### Issue 2 — Filebeat: no enabled filesets
**Cause:** Enabling the system module does not automatically enable its filesets.
**Fix:** Edited `/etc/filebeat/modules.d/system.yml` and set syslog and auth to `enabled: true`.

### Issue 3 — Kibana connection timeout after network change
**Cause:** Kibana had a hardcoded local IP that became invalid after switching networks.
**Fix:** Changed `elasticsearch.hosts` in kibana.yml from the local IP to `localhost`.

### Issue 4 — Elasticsearch OOM killed
**Cause:** Elasticsearch consumed 7.9GB of RAM and was killed by the Linux OOM killer.
**Fix:** Created `/etc/elasticsearch/jvm.options.d/memory.options` and capped heap to 512MB.

### Issue 5 — Filebeat x509 certificate error
**Cause:** Filebeat was not configured to trust Elasticsearch's self-signed certificate.
**Fix:** Added `ssl.verification_mode: none` to the output.elasticsearch block in filebeat.yml.

## Key Learnings
- How data flows through the stack: Filebeat → Elasticsearch → Kibana
- How Elasticsearch uses indices and data streams to organize data
- How to troubleshoot services using systemctl and journalctl
- How to authenticate and interact with a secured Elasticsearch cluster via REST API
- How to tune JVM heap size to prevent OOM kills in memory-constrained environments
