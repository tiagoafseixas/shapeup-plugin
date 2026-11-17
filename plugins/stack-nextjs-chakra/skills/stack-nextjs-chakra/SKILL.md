---
name: stack-nextjs-chakra
description: Stack pack for the shapeup-team plugin — Next.js App Router frontends styled with Chakra UI v3. Loaded by the frontend-dev agent when the team config (team.md) › Roles names stack-nextjs-chakra. Also use it when writing or reviewing Next.js or Chakra UI code in a repo set up by the shapeup-team plugin.
---

# Stack pack: Next.js App Router + Chakra UI v3

| Layer | Covers | Agent |
|---|---|---|
| frontend | Next.js 14–16 (App Router), React 18–19, Chakra UI v3 | frontend-dev |

The role file says what to do and when (tests first, handoffs, gates); this pack says how, in this stack.
House rules in the repo (`<docs>/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.

## Version notes

| Version | Watch for |
|---|---|
| Chakra v3 vs v2 | Almost every API changed: `css` not `sx`, `disabled` not `isDisabled`, compound components (`Dialog.Root`, `Field.Label`), `createSystem` instead of `extendTheme`, snippets in `components/ui/`. Use v3 docs only. |
| Next.js majors | The docs default to the latest major. For an older one, put the version in the path (`https://nextjs.org/docs/15/app/...`). |
| React 19 | Actions, `useActionState`, `use()`; `forwardRef` no longer needed for refs on function components |

## Layering

| Logic | Goes in | Never in |
|---|---|---|
| Route, data loading for the page, metadata | `app/**/page.js` / `layout.js` as Server Components | A client component's `useEffect` |
| Interactivity: state, effects, browser APIs | The smallest leaf marked `'use client'` | The page or layout |
| Calls to the API | A per-domain API module, wrapped by TanStack Query hooks (one key per resource) | Components |
| Reusable UI | A house component (including Chakra snippets in `components/ui/`) | Copies in each screen |
| Visual variants reused across components | A recipe or slot recipe in the system/theme file | Props spread across screens |
| Secrets and server-only tokens | Server Components, route handlers, server actions | Anything imported by a client component |

Build order for a component, stop at the first that works:

1. A house component already in the repo, including the Chakra snippets in `components/ui/` (search before you build)
2. A Chakra v3 component, configured with props and its recipe variants
3. The `chakra()` factory around a native element or third-party component, styled with tokens
4. A new component, beside its only user until a second user exists

## Rules

| Area | Rule |
|---|---|
| Server vs client | Keep pages and layouts as Server Components unless they need state, effects or browser APIs. Follow the repo where it already makes whole pages client-side; don't refactor that inside a scope. |
| Theme | Colours, spacing, radii, typography and shadows come from tokens. Prefer semantic tokens (`fg.muted`, `bg.panel`, `border`) so dark mode works. No hex values, px spacing or font sizes in components. A new token or recipe variant goes in the system file, logged as `DECIDE`. |
| Styling | Style props for simple cases, the `css` prop for nested selectors and states, recipes for variants. No inline `style={}`, no new CSS files unless the repo uses them. |
| Server data | TanStack Query: invalidate on mutation, `refetchInterval` for polling jobs. No `fetch` inside `useEffect` in new code. |
| Forms | The repo's form library (Formik + Yup, or React Hook Form + Zod). Map API field errors to fields with `Field.ErrorText`; disable submit while pending. |
| Accessibility | `Field.Label` on every input, `aria-label` on icon-only buttons, Chakra's dialog focus handling untouched, focus ring kept |
| Images and heavy widgets | `next/image` for images, `next/dynamic` for heavy client-only widgets |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | The repo's runner (Vitest, Jest or `node --test`) on pure modules | No DOM, no network: pure functions, schemas, mappers, hooks without I/O. List slow tests with the runner's reporter. |
| Medium | Testing Library (`@testing-library/react`, `user-event`) with the Chakra provider; MSW for the API, or Cypress component tests with `cy.intercept` | API mocked at the network; queries by role, label or text. Async Server Components aren't supported by Testing Library: cover them in Large tests. |
| Large | Playwright or Cypress against `next build && next start` and the real API | Stub only external systems (payments, Google, analytics) at the network edge |

## Performance

| Rule | How |
|---|---|
| Ship less JavaScript | Keep the `'use client'` boundary low; `next/dynamic` for heavy client-only widgets |
| Images and fonts | `next/image` with sizes; `next/font` |
| Re-renders | Memoise only to fix a measured problem (React DevTools Profiler) |
| Data | Cache and dedupe through TanStack Query keys; no request waterfalls between parent and child |

## Review checklist

| Finding | Sev |
|---|---|
| A secret or server-only module imported into a client component | `must` |
| An input without a label, or an icon-only button without `aria-label` | `must` |
| A Chakra v2 API (`sx`, `isDisabled`, `extendTheme`) in new code | `should` |
| A hex colour, px spacing or font size in a component | `should` |
| `'use client'` on a page or layout that only needs one interactive leaf | `should` |
| `fetch` in `useEffect` in new code | `should` |

## Sources

Indexed in `references/sources.md`: the main Next.js App Router pages and the Chakra UI v3 docs, plus the testing tools above.
