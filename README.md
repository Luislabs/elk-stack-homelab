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
