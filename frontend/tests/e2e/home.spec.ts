import { expect, test } from "@playwright/test";

test.describe("AgriGuard AI E2E Critical Journeys", () => {
	test.beforeEach(async ({ page }) => {
		// Set a desktop viewport so desktop navigation bar is visible
		await page.setViewportSize({ width: 1280, height: 800 });
		// Mock API boundary for deterministic offline E2E testing
		await page.route("**/api/v1/farms", (route) =>
			route.fulfill({
				status: 200,
				contentType: "application/json",
				body: JSON.stringify([]),
			}),
		);
		await page.route("**/api/v1/advisories", (route) =>
			route.fulfill({
				status: 200,
				contentType: "application/json",
				body: JSON.stringify([]),
			}),
		);
	});

	test("has title and main dashboard heading", async ({ page }) => {
		await page.goto("/");
		await expect(page).toHaveTitle(/AgriGuard AI/);
		const heading = page.getByRole("heading", { level: 1 });
		await expect(heading).toBeVisible();
	});

	test("can navigate to farm setup and view onboarding form", async ({
		page,
	}) => {
		await page.goto("/");
		await page.getByRole("link", { name: "Farms", exact: true }).click();
		await expect(page).toHaveURL(/\/farm/);
		await expect(
			page.getByRole("heading", { name: /Farm Setup/i }),
		).toBeVisible();
	});

	test("can navigate to soil health analysis page", async ({ page }) => {
		await page.goto("/");
		await page.getByRole("link", { name: "Soil Health", exact: true }).click();
		await expect(page).toHaveURL(/\/soil/);
		await expect(
			page.getByRole("heading", { name: /Soil Health Analysis/i }),
		).toBeVisible();
	});

	test("can navigate to crop disease inference page", async ({ page }) => {
		await page.goto("/");
		await page.getByRole("link", { name: "Crop Disease", exact: true }).click();
		await expect(page).toHaveURL(/\/disease/);
		await expect(
			page.getByRole("heading", { name: /Crop Leaf Disease Inference/i }),
		).toBeVisible();
	});

	test("can navigate to advisory history page", async ({ page }) => {
		await page.goto("/");
		await page
			.getByRole("link", { name: "Advisory History", exact: true })
			.click();
		await expect(page).toHaveURL(/\/history/);
		await expect(
			page.getByRole("heading", { name: /Advisory Audit Trail/i }),
		).toBeVisible();
	});

	test("can navigate to responsible AI governance page", async ({ page }) => {
		await page.goto("/");
		await page
			.getByRole("link", { name: "Responsible AI", exact: true })
			.click();
		await expect(page).toHaveURL(/\/responsible-ai/);
		await expect(
			page.getByRole("heading", { name: /Responsible AI/i }),
		).toBeVisible();
	});
});
