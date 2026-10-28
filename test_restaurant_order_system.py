"""Behavioral regression tests for the restaurant lab."""

import copy
import tempfile
import unittest
from pathlib import Path

import restaurant_order_system as restaurant


class RestaurantTests(unittest.TestCase):
    """Preserve order behavior and verify security boundaries."""

    def setUp(self):
        self.original = copy.deepcopy(restaurant.orders)

    def tearDown(self):
        restaurant.orders.clear()
        restaurant.orders.update(self.original)

    def test_create_duplicate_and_invalid_orders(self):
        log = []
        self.assertTrue(restaurant.place_table_order("T9", "Guest", 2, log))
        self.assertEqual(restaurant.orders["T9"]["bill"], 30.0)
        self.assertEqual(len(log), 1)
        self.assertFalse(restaurant.place_table_order("T9", "Guest", 2))
        self.assertFalse(restaurant.place_table_order("T8", "Guest", 0))

    def test_logging_is_optional_and_caller_owned(self):
        log = []
        restaurant.place_table_order("T8", "Guest", 1, log)
        restaurant.place_table_order("T9", "Guest", 1)
        self.assertEqual(len(log), 1)
        self.assertIsNone(restaurant.place_table_order.__defaults__[0])

    def test_void_and_status(self):
        self.assertTrue(restaurant.check_table_status("T1"))
        self.assertFalse(restaurant.check_table_status("T2"))
        restaurant.void_table_order("T1")
        restaurant.void_table_order("missing")
        self.assertFalse(restaurant.check_table_status("T1"))
        self.assertEqual(restaurant.get_pending_summary(restaurant.orders), 1)

    def test_discount_boundaries(self):
        self.assertEqual(restaurant.calculate_discounted_bill("T1", .1), 40.5)
        self.assertEqual(restaurant.calculate_discounted_bill("T1", 0), 45)
        self.assertEqual(restaurant.calculate_discounted_bill("T1", 1), 0)
        for rate in (-.1, 1.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                restaurant.calculate_discounted_bill("T1", rate)
        with self.assertRaises(TypeError):
            restaurant.calculate_discounted_bill("T1", "base_bill * 0.9")
        with self.assertRaises(KeyError):
            restaurant.calculate_discounted_bill("missing", .1)

    def test_hash_and_pin(self):
        ticket = restaurant.generate_ticket_hash("T1")
        self.assertEqual(len(ticket), 64)
        self.assertEqual(ticket, restaurant.generate_ticket_hash("T1"))
        self.assertNotEqual(ticket, restaurant.generate_ticket_hash("T2"))
        for _ in range(100):
            self.assertIn(restaurant.generate_pos_pin(), range(1000, 10000))

    def test_export_treats_shell_characters_as_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "orders & echo injected.txt"
            restaurant.export_kitchen_orders(filename)
            self.assertEqual(filename.read_text(encoding="utf-8"),
                             str(restaurant.orders))


if __name__ == "__main__":
    unittest.main()
