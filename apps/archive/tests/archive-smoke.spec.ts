import { expect, test } from "@playwright/test";

test("home exposes primary archive navigation", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/MSCS Playbook Archive/);
  await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Browse" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 1, name: /curriculum archive with search/i })).toBeVisible();
  await expect(page.locator("main")).toBeVisible();
});

test("browse supports search and filters", async ({ page }) => {
  await page.goto("/browse");
  await page.locator("#query").fill("policy gradient");
  await expect(page.locator("#results")).toContainText("Policy Gradient and Actor-Critic Methods");

  await page.locator("#module").selectOption("14-reinforcement-learning");
  await expect(page.locator("#results")).toContainText("Reinforcement Learning");
  await expect(page.locator("#results-count")).not.toHaveText(/Showing 0 results/);
  await expect(page).toHaveURL(/q=policy\+gradient/);
  await expect(page).toHaveURL(/module=14-reinforcement-learning/);
});

test("document page renders toc, source link, and sequence navigation", async ({ page }) => {
  await page.goto("/modules/11-generative-ai/01-concepts/04-rag-design-chunking-indexing-and-retrieval");
  await expect(page.locator("main h1")).toHaveCount(1);
  await expect(page.locator("section h1").first()).toHaveText(/RAG Design/i);
  await expect(page.getByRole("link", { name: /View source on GitHub/i })).toBeVisible();
  await expect(page.getByText("On this page")).toBeVisible();
  await expect(page.getByText("Continue through the reading path")).toBeVisible();
});

test("track and project hubs expose linked archive entities", async ({ page }) => {
  await page.goto("/tracks/ai-engineer");
  await expect(page.locator("main h1")).toHaveCount(1);
  await expect(page.locator("section h1").first()).toHaveText(/AI Engineer Track/i);
  await expect(page.locator('a[href="/projects/p7-genai-rag-agent-app"]').first()).toBeVisible();

  await page.goto("/projects/p7-genai-rag-agent-app");
  await expect(page.locator("main h1")).toHaveCount(1);
  await expect(page.locator("section h1").first()).toHaveText(/p7-genai-rag-agent-app/i);
  await expect(page.getByRole("link", { name: /Generative AI/i }).first()).toBeVisible();
});

test("mobile browse remains usable", async ({ page }) => {
  await page.goto("/browse?q=nat");
  await expect(page.getByRole("heading", { level: 1, name: /Search the archive/i })).toBeVisible();
  await expect(page.locator("#results")).toContainText("Firewalling and NAT");
});

test("docs hub links into archive application routes", async ({ page }) => {
  await page.goto("/docs");
  await expect(page.getByRole("link", { name: /archive browse surface/i })).toHaveAttribute("href", "/browse");
  await expect(page.getByRole("link", { name: /tracks hub/i })).toHaveAttribute("href", "/tracks");
});
