import os
import json

def add_anomaly(info):
    with open('anomalies/registry.json', encoding='utf-8') as f:
        registry = json.load(f)
    if not info in registry:
        registry.append(info)
    with open('anomalies/registry.json','w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False)

def get_anomalies():
    with open('anomalies/registry.json', encoding='utf-8') as f:
        registry = json.load(f)
    return registry