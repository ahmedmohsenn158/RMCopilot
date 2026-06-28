from backend.infrastructure.data_access import events_for_customer, load_customers


def get_customer(customer_id: str) -> dict | None:
    return next((c for c in load_customers() if c["customer_id"] == customer_id), None)


def search_customers(rm_id: str, query: str = "") -> list[dict]:
    customers = [c for c in load_customers() if c.get("rm_id") == rm_id]
    if not query:
        return customers

    q = query.lower()
    return [
        c
        for c in customers
        if q in c["name"].lower()
        or q in c["segment"].lower()
        or q in c["tier"].lower()
        or q in c["account_no"].lower()
        or q in c["customer_id"].lower()
    ]


def to_customer_search_item(customer: dict) -> dict:
    tier = customer.get("tier", "")
    status = "alert" if customer["customer_id"] == "cust_khaled_001" else "active"
    if customer["customer_id"] == "cust_mohamed_003":
        status = "review"
    if customer["customer_id"] == "cust_layla_004":
        status = "inactive"

    return {
        "id": customer["customer_id"],
        "name": customer["name"],
        "initials": customer.get("initials", ""),
        "segment": f"{customer['segment']} {tier}".strip(),
        "accountNo": customer.get("account_no", ""),
        "color": _color_for_tier(tier),
        "status": status,
        "statusLabel": status.title() if status != "review" else "Review due",
    }


def to_active_customer(customer: dict) -> dict:
    events = events_for_customer(customer["customer_id"])
    breach = next((e for e in events if e.get("event_type") == "credit_limit_breach"), None)
    expiry = next((e for e in events if e.get("event_type") == "product_expiry"), None)

    credit_util = breach["utilisation_pct"] if breach else customer["baseline"].get("avg_credit_utilisation_pct", 0)
    return {
        "id": customer["customer_id"],
        "name": customer["name"],
        "initials": customer.get("initials", ""),
        "segment": customer["segment"],
        "tier": customer["tier"],
        "joinedYear": customer["joined"][:4],
        "stats": [
            {"label": "Total balance", "value": "EGP 2.4M", "color": "default"},
            {"label": "Credit util.", "value": f"{credit_util}%", "color": "danger" if credit_util > 90 else "default"},
            {"label": "Active products", "value": str(len(customer.get("products", []))), "color": "default"},
            {"label": "Open actions", "value": str(len(customer.get("crm", {}).get("open_actions", []))), "color": "warning"},
        ],
        "tags": _tags_for_customer(customer, expiry),
        "lastContact": f"{customer['crm']['last_contact']} - {customer['crm']['last_topic']}",
        "nextMeeting": customer["crm"].get("next_meeting"),
        "raw": customer,
    }


def _tags_for_customer(customer: dict, expiry: dict | None) -> list[dict]:
    tags = [{"label": p.replace("_", " ").title(), "color": "accent"} for p in customer.get("products", [])]
    if "fx_forward_contract" not in customer.get("products", []):
        tags.append({"label": "No FX hedging", "color": "muted"})
    if expiry:
        tags.append({"label": f"{expiry['product'].replace('_', ' ').title()} expiring", "color": "warning"})
    return tags


def _color_for_tier(tier: str) -> str:
    return {
        "Gold": "accent",
        "Silver": "success",
        "Platinum": "warning",
    }.get(tier, "muted")
