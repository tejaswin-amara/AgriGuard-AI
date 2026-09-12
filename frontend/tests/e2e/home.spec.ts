import { expect, test } from "@playwright/test";

test("has title and main heading", async ({ page }) => {
	await page.goto("/");

	// Check the title
	await expect(page).toHaveTitle(/AgriGuard AI/);

	// Check that the heading is present (in English 'AgriGuard AI' or corresponding translation)
	const heading = page.getByRole("heading", { level: 1 });
	await expect(heading).toBeVisible();
});
