"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create a unique table order and optionally append to a caller's log."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": 15.0 * items_count,
        "is_settled": False,
    }
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Remove a table order; a missing table is an intentional no-op."""
    orders.pop(table_id, None)


def check_table_status(table_id):
    """Return whether the table exists and has an unsettled bill."""
    order = orders.get(table_id)
    return order is not None and not order["is_settled"]


def calculate_discounted_bill(table_id, discount_rate):
    """Apply a fractional discount in [0, 1]; unknown tables raise KeyError."""
    base_bill = orders[table_id]["bill"]
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    return round(base_bill * (1 - discount_rate), 2)


def generate_ticket_hash(table_id):
    """Return a SHA-256 ticket identifier, not an authentication credential."""
    return hashlib.sha256(table_id.encode("utf-8")).hexdigest()


def generate_pos_pin():
    """Generate a four-digit PIN using a cryptographic randomness source."""
    return 1000 + secrets.randbelow(9000)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write the orders as UTF-8 text without invoking a shell."""
    with open(filename, "w", encoding="utf-8") as order_file:
        order_file.write(str(orders))
    print("Ticket exported for kitchen printer:", filename)


def get_pending_summary(table_orders):
    """Count unsettled orders in the supplied mapping."""
    return sum(not details["is_settled"] for details in table_orders.values())


def main():
    """Execute sample restaurant billing operations."""
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 0.10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))


if __name__ == "__main__":
    main()
