# KB: Next.js (App Router) + Chakra UI v3

Check the installed majors in `package.json` first. The Next docs default to the latest major. For an older major,
insert the version in the path (`https://nextjs.org/docs/15/app/...`). Chakra v3 differs from v2 in almost every API:
use only v3 pages. Where a source conflicts with `roles/frontend-react.md`, the role file wins.

## Next.js: Getting Started (App Router)

| Page | URL | Use it for |
|---|---|---|
| Docs index (all pages, machine-readable) | https://nextjs.org/docs/llms.txt | Finding any page fast |
| Project structure | https://nextjs.org/docs/app/getting-started/project-structure | Folder conventions, route groups, colocation |
| Layouts and pages | https://nextjs.org/docs/app/getting-started/layouts-and-pages | `page.js`, `layout.js`, dynamic segments |
| Linking and navigating | https://nextjs.org/docs/app/getting-started/linking-and-navigating | `<Link>`, prefetching, `useRouter` |
| Server and Client Components | https://nextjs.org/docs/app/getting-started/server-and-client-components | Where `'use client'` goes; keep the boundary low to shrink bundles |
| Fetching data | https://nextjs.org/docs/app/getting-started/fetching-data | Server fetch, streaming with `<Suspense>`, client fetching with React Query |
| Mutating data | https://nextjs.org/docs/app/getting-started/mutating-data | Server Functions / Actions vs API calls |
| Caching / Revalidating | https://nextjs.org/docs/app/getting-started/caching · https://nextjs.org/docs/app/getting-started/revalidating | What is cached, and how to refresh it |
| Error handling | https://nextjs.org/docs/app/getting-started/error-handling | `error.js`, `not-found.js`, expected vs unexpected errors |
| CSS · Images · Fonts | https://nextjs.org/docs/app/getting-started/css · https://nextjs.org/docs/app/getting-started/images · https://nextjs.org/docs/app/getting-started/fonts | Asset optimisation |
| Metadata and OG images | https://nextjs.org/docs/app/getting-started/metadata-and-og-images | SEO for public pages |
| Route handlers | https://nextjs.org/docs/app/getting-started/route-handlers | `route.js` endpoints (only when the Django API can't serve it) |
| Proxy (formerly middleware) | https://nextjs.org/docs/app/getting-started/proxy | Redirects and auth checks before render |
| Deploying · Upgrading | https://nextjs.org/docs/app/getting-started/deploying · https://nextjs.org/docs/app/getting-started/upgrading | Release and major-version moves |

## Next.js: Guides and reference

| Page | URL | Use it for |
|---|---|---|
| Guides index | https://nextjs.org/docs/app/guides | Auth, forms, i18n, testing, production checklist |
| Data security | https://nextjs.org/docs/app/guides/data-security | Authorising server-side data access |
| API reference index | https://nextjs.org/docs/app/api-reference | File conventions, functions, `next.config.js`, directives |
| `fetch` reference | https://nextjs.org/docs/app/api-reference/functions/fetch | Cache options per request |
| `loading.js` | https://nextjs.org/docs/app/api-reference/file-conventions/loading | Route-level loading UI |
| Next 15 docs (pinned) | https://nextjs.org/docs/15/app/getting-started/fetching-data | Pattern for reading docs of the installed major |

## Chakra UI v3: Get started

| Page | URL | Use it for |
|---|---|---|
| Installation | https://www.chakra-ui.com/docs/get-started/installation | Provider setup, snippets |
| Next.js (App Router) | https://www.chakra-ui.com/docs/get-started/frameworks/next-app | Client Provider in `layout`, hydration, color mode |
| Migration v2 → v3 | https://www.chakra-ui.com/docs/get-started/migration | Renamed props and components (e.g. `sx` → `css`, `isDisabled` → `disabled`) |
| CLI (snippets, typegen) | https://www.chakra-ui.com/docs/get-started/cli | Adding component snippets, theme typings |
| LLMs.txt · MCP server | https://www.chakra-ui.com/docs/get-started/ai/llms · https://www.chakra-ui.com/docs/get-started/ai/mcp-server | Feeding exact v3 docs to an agent |
| Components overview | https://www.chakra-ui.com/docs/components/concepts/overview | The component catalogue |
| Charts | https://www.chakra-ui.com/docs/charts/installation | Charts consistent with the theme |

## Chakra UI v3: Styling

| Page | URL | Use it for |
|---|---|---|
| Styling overview | https://www.chakra-ui.com/docs/styling/overview | Style props vs `css` prop |
| Responsive design | https://www.chakra-ui.com/docs/styling/responsive-design | Breakpoint objects and arrays |
| Dark mode · Conditional styles | https://www.chakra-ui.com/docs/styling/dark-mode · https://www.chakra-ui.com/docs/styling/conditional-styles | `_dark`, `_hover`, pseudo states |
| Chakra factory | https://www.chakra-ui.com/docs/styling/chakra-factory | Styling a native element or third-party component |
| CSS variables · Cascade layers | https://www.chakra-ui.com/docs/styling/css-variables · https://www.chakra-ui.com/docs/styling/cascade-layers | Overrides without specificity fights |
| Text styles · Layer styles | https://www.chakra-ui.com/docs/styling/text-styles · https://www.chakra-ui.com/docs/styling/layer-styles | Reusable typography and surfaces |
| Focus ring | https://www.chakra-ui.com/docs/styling/focus-ring | Accessible focus states |
| Style props (spacing, layout, flex/grid, typography…) | https://www.chakra-ui.com/docs/styling/style-props/spacing | Prop reference; sibling pages under `/style-props/` |

## Chakra UI v3: Theming

| Page | URL | Use it for |
|---|---|---|
| Theming overview | https://www.chakra-ui.com/docs/theming/overview | `createSystem`, `defineConfig` |
| Tokens · Semantic tokens | https://www.chakra-ui.com/docs/theming/tokens · https://www.chakra-ui.com/docs/theming/semantic-tokens | Raw values vs meaning (`fg.muted`, `bg.panel`); light/dark |
| Recipes · Slot recipes | https://www.chakra-ui.com/docs/theming/recipes · https://www.chakra-ui.com/docs/theming/slot-recipes | Variants for single- and multi-part components |
| Colors · Spacing · Typography · Breakpoints | https://www.chakra-ui.com/docs/theming/colors · https://www.chakra-ui.com/docs/theming/spacing · https://www.chakra-ui.com/docs/theming/typography · https://www.chakra-ui.com/docs/theming/breakpoints | Default scales |
| Customization overview | https://www.chakra-ui.com/docs/theming/customization/overview | Extending the default system |
| Customize recipes · colors · conditions | https://www.chakra-ui.com/docs/theming/customization/recipes · https://www.chakra-ui.com/docs/theming/customization/colors · https://www.chakra-ui.com/docs/theming/customization/conditions | Changing components without forking them |
| Global CSS | https://www.chakra-ui.com/docs/theming/customization/global-css | App-wide base styles |

## React, data and quality

| Source | URL | Use it for |
|---|---|---|
| You Might Not Need an Effect | https://react.dev/learn/you-might-not-need-an-effect | Removing effects for derived state |
| Rules of React | https://react.dev/reference/rules | Purity and hooks rules |
| TanStack Query | https://tanstack.com/query/latest | Server state: keys, invalidation, polling |
| Formik · Yup | https://formik.org/docs/overview · https://github.com/jquense/yup | Forms and schemas, if the repo uses them |
| Cypress best practices | https://docs.cypress.io/app/core-concepts/best-practices | E2E selectors and isolation |
| WAI-ARIA Authoring Practices | https://www.w3.org/WAI/ARIA/apg/ | Keyboard and ARIA patterns |
