import unittest

from validators import validate_inputs


class ValidatorsTest(unittest.TestCase):
    def test_valid_long_setup_has_no_errors(self):
        errors = validate_inputs(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=95,
            leverage=10,
            risk_percent=2,
        )

        self.assertEqual(errors, [])

    def test_valid_short_setup_has_no_errors(self):
        errors = validate_inputs(
            account_balance=1000,
            direction="Short",
            entry_price=100,
            stop_price=105,
            leverage=10,
            risk_percent=2,
        )

        self.assertEqual(errors, [])

    def test_rejects_non_positive_inputs_and_invalid_risk(self):
        errors = validate_inputs(
            account_balance=0,
            direction="Long",
            entry_price=0,
            stop_price=0,
            leverage=0.5,
            risk_percent=12,
        )

        self.assertIn("Account balance must be greater than 0.", errors)
        self.assertIn("Entry price must be greater than 0.", errors)
        self.assertIn("Stop price must be greater than 0.", errors)
        self.assertIn("Leverage must be at least 1x.", errors)
        self.assertIn("Risk percentage must be greater than 0 and no more than 10.", errors)

    def test_rejects_stop_equal_to_entry(self):
        errors = validate_inputs(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=100,
            leverage=10,
            risk_percent=2,
        )

        self.assertIn("Stop price must not equal entry price.", errors)

    def test_rejects_long_stop_above_entry(self):
        errors = validate_inputs(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=105,
            leverage=10,
            risk_percent=2,
        )

        self.assertIn("For a Long trade, the stop price should be below entry price.", errors)

    def test_rejects_short_stop_below_entry(self):
        errors = validate_inputs(
            account_balance=1000,
            direction="Short",
            entry_price=100,
            stop_price=95,
            leverage=10,
            risk_percent=2,
        )

        self.assertIn("For a Short trade, the stop price should be above entry price.", errors)


if __name__ == "__main__":
    unittest.main()
