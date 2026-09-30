# AgriGuard AI Frontend

React + TypeScript frontend for the AgriGuard AI prototype.

## Stack

- React 19
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS
- i18next / react-i18next
- Biome
- Playwright

## Application pages

The current router exposes:

| Path | Page |
|---|---|
| `/` | Farm Intelligence Dashboard |
| `/farm` | Farm Setup |
| `/soil` | Soil Health Analysis |
| `/disease` | Crop Leaf Disease Inference |
| `/insights` | Insights |
| `/history` | Advisory Audit Trail |
| `/responsible-ai` | Responsible AI |
| `/about` | About |

## Development

```bash
npm ci
npm run dev
```

## Build

```bash
npm run build
```

The build runs TypeScript compilation followed by Vite production bundling.

## Linting / formatting

```bash
npm run lint
npx biome ci .
```

## End-to-end tests

The Playwright configuration:

- targets Chromium;
- uses `tests/e2e`;
- serves the production build through Vite preview on port 4173;
- mocks selected API boundaries for deterministic tests.

Run:

```bash
npx playwright install --with-deps chromium
npx playwright test
```

## API configuration

The Axios client uses the relative base URL:

```text
/api/v1
```

The current Vite configuration does not define an API proxy, and the Dockerized Nginx frontend does not contain a backend reverse-proxy rule. When running the frontend separately, use a development/reverse-proxy arrangement that makes `/api/v1` reachable by the browser.

## Current frontend limitations

The frontend is a prototype UI. It should not imply that disease or soil outputs are validated agricultural predictions.
