from app import app

print("=== Defined Routes in ShopEase ===")
print("Route -> Endpoint")
print("-" * 40)

for rule in app.url_map.iter_rules():
    methods = ','.join(rule.methods)
    print(f"{rule.rule} -> {rule.endpoint} [{methods}]")

print("\n=== All Endpoints ===")
endpoints = sorted([rule.endpoint for rule in app.url_map.iter_rules()])
for endpoint in endpoints:
    print(f"  - {endpoint}")

print(f"\nTotal routes: {len(list(app.url_map.iter_rules()))}")