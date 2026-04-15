import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3

# Suppress SSL warnings since we're using self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── CONFIG ──────────────────────────────────────────────────────────────────
HOST     = "https://localhost:9200"
USERNAME = "elastic"
PASSWORD = "123456"
AUTH     = HTTPBasicAuth(USERNAME, PASSWORD)
# ────────────────────────────────────────────────────────────────────────────

def query(endpoint, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    try:
        r = requests.get(f"{HOST}{endpoint}", auth=AUTH, verify=False)
        data = r.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"  ERROR: {e}")

def main():
    print("\n" + "="*60)
    print("   ELASTICSEARCH CLUSTER DISCOVERY REPORT")
    print("="*60)
    print(f"   Target: {HOST}")
    print("="*60)

    query("/",                      "CLUSTER IDENTITY & VERSION")
    query("/_cluster/health",       "CLUSTER HEALTH")
    query("/_cat/indices?v&h=index,health,status,docs.count,store.size&format=json", "INDICES")
    query("/_nodes?filter_path=nodes.*.name,nodes.*.ip,nodes.*.version,nodes.*.roles", "NODES")
    query("/_cluster/settings?pretty&include_defaults=false", "CLUSTER SETTINGS")

    print(f"\n{'='*60}")
    print("   END OF REPORT")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
