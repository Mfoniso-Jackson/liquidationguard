import unittest

from risk_engine import calculate_risk, get_safety_status


class RiskEngineTest(unittest.TestCase):
    def test_long_trade_core_calculations(self):
        result = calculate_risk(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=95,
            leverage=10,
            risk_percent=2,
        )

        self.assertEqual(result["risk_per_unit"], 5)
        self.assertEqual(result["max_risk_amount"], 20)
        self.assertEqual(result["position_size_units"], 4)
        self.assertEqual(result["notional_position_value"], 400)
        self.assertEqual(result["margin_required"], 40)
        self.assertEqual(result["money_at_risk"], 20)
        self.assertEqual(result["account_risk_percent"], 2)
        self.assertEqual(result["liquidation_price"], 90)
        self.assertEqual(result["distance_to_stop_percent"], 5)
        self.assertEqual(result["distance_to_liquidation_percent"], 10)
        self.assertFalse(result["liquidation_vs_stop_warning"])
        self.assertEqual(result["safety_status"], "Moderate")

    def test_short_trade_liquidation_calculation(self):
        result = calculate_risk(
            account_balance=5000,
            direction="Short",
            entry_price=2000,
            stop_price=2100,
            leverage=20,
            risk_percent=1,
        )

        self.assertEqual(result["position_size_units"], 0.5)
        self.assertEqual(result["liquidation_price"], 2100)
        self.assertEqual(result["distance_to_liquidation_percent"], 5)
        self.assertEqual(result["safety_status"], "Conservative")

    def test_liquidation_closer_than_stop_adds_warning_and_decision(self):
        result = calculate_risk(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=80,
            leverage=10,
            risk_percent=2,
        )

        self.assertTrue(result["liquidation_vs_stop_warning"])
        self.assertIn(
            "Liquidation is closer to entry than your stop loss.",
            result["warnings"],
        )
        self.assertIn("dangerous", result["decision"])

    def test_margin_exceeds_account_balance_warning(self):
        result = calculate_risk(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=99,
            leverage=1,
            risk_percent=10,
        )

        self.assertGreater(result["margin_required"], 1000)
        self.assertIn("Margin required exceeds your account balance.", result["warnings"])

    def test_high_leverage_warning(self):
        result = calculate_risk(
            account_balance=1000,
            direction="Short",
            entry_price=100,
            stop_price=101,
            leverage=25,
            risk_percent=2,
        )

        self.assertIn("Leverage is above 20x.", result["warnings"])
        self.assertIn("leverage is high", result["decision"])

    def test_safety_status_thresholds(self):
        self.assertEqual(get_safety_status(1), "Conservative")
        self.assertEqual(get_safety_status(3), "Moderate")
        self.assertEqual(get_safety_status(3.01), "High Risk")


if __name__ == "__main__":
    unittest.main()
