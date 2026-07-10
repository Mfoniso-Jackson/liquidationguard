import { expect, test } from "@playwright/test";

test("calculates risk successfully", async ({ page }) => {
  await page.route("**/api/risk/calculate", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        calculation_id: "test-calculation",
        result: {
          risk_per_unit: 5,
          max_risk_amount: 20,
          position_size_units: 4,
          notional_position_value: 400,
          margin_required: 40,
          money_at_risk: 20,
          account_risk_percent: 2,
          liquidation_price: 90,
          distance_to_stop_percent: 5,
          distance_to_liquidation_percent: 10,
          liquidation_vs_stop_warning: false,
          safety_status: "Moderate",
          warnings: ["Liquidation estimate is approximate."],
          interpretation: "This setup fits your chosen risk level.",
        },
      }),
    });
  });
  await page.route("**/api/waitlist", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        id: "waitlist-test",
        status: "joined",
      }),
    });
  });

  await page.goto("/");
  await page.getByRole("link", { name: "Calculate Risk" }).click();
  await page.getByRole("button", { name: "Calculate Risk" }).click();

  await expect(page.getByText("Trade decision")).toBeVisible();
  await expect(page.getByText("Suggested position size")).toBeVisible();
  await expect(page.getByText("4.0000")).toBeVisible();
  await expect(page.getByText("Copy Summary")).toBeVisible();

  await page.getByRole("textbox", { name: "Email", exact: true }).fill("trader@example.com");
  await page.getByRole("button", { name: "Join Pro Waitlist" }).click();
  await expect(page.getByText("You're on the Pro waitlist.")).toBeVisible();
});
