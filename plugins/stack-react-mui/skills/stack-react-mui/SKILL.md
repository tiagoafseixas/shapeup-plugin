---
name: stack-react-mui
description: Stack pack for the shapeup-team plugin — React frontends built with Material UI (MUI) v7 and v9, in Vite or Next.js. Loaded by the frontend-dev agent when the team config (team.md) › Roles names stack-react-mui. Also use it when writing or reviewing Material UI code (theme, sx, styled, slots, Grid, MUI X Data Grid) in a repo set up by the shapeup-team plugin.
---

# Stack pack: React + Material UI

| Layer | Covers | Agent |
|---|---|---|
| frontend | React 18–19, Material UI v7 and v9 (`@mui/material`), MUI X v9, Vite or Next.js | frontend-dev |

The role file says what to do and when (tests first, handoffs, gates); this pack says how, in this stack.
House rules in the repo (`<docs>/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.

## Version notes

Check `@mui/material` in `package.json` first. There is no Material UI v8: it went from v7 to v9 (April 2026) to share a major with MUI X.

| Change | v7 | v9 |
|---|---|---|
| Grid | `Grid` with `size={{ xs: 12, md: 6 }}`; `GridLegacy` still there | `GridLegacy` removed; `Grid` `direction="column"` removed (use `Stack`) |
| System props (`mt`, `color`, `p` as props) | Deprecated on Box, Stack, Typography | Removed: use `sx`. Codemod: `npx @mui/codemod@latest v9.0.0/system-props <path>` |
| Customising inner parts | `slots` / `slotProps` preferred; `components`, `componentsProps`, `PaperProps`, `TransitionComponent` deprecated | The deprecated props are removed: `slots` / `slotProps` only |
| TextField inner props | `InputProps`, `inputProps`, `InputLabelProps` deprecated | Removed: `slotProps={{ input, htmlInput, inputLabel, formHelperText, select }}` |
| Dialog / Modal | `disableEscapeKeyDown` deprecated | Removed: check `reason` in `onClose` |
| Keyboard | — | Roving `tabindex` in Tabs, Menu and Stepper; `Tab` outside `Tabs` throws; `MenuItem` must sit inside `Menu` or `MenuList` |
| Browsers | Chrome 109, Safari 15.4 | Chrome 117, Safari 17 |

Per-deprecation codemods: `npx @mui/codemod@latest deprecations/<name> <path>`. Write new code with v9 APIs even on v7: they already work there.

## Layering

| Logic | Goes in | Never in |
|---|---|---|
| Palette, typography, shape, spacing, breakpoints, light and dark schemes | One theme file: `createTheme({ cssVariables: true, colorSchemes: { light, dark } })` | Components |
| Default props and look of a component across the app | `theme.components.Mui<Name>.defaultProps` / `styleOverrides` / `variants` | Copies of the same `sx` in each screen |
| One-off style on one element | The `sx` prop, reading tokens (`color: 'text.secondary'`, `p: 2`) | Inline `style={}` |
| A styled building block reused in several places | `styled()` from `@mui/material/styles`, with `shouldForwardProp` for custom props | A wrapper that spreads `sx` everywhere |
| Inner parts of a component (paper, input, backdrop, transition) | `slots` and `slotProps` | Deprecated `*Props` and `components` props |
| Global CSS (resets, body, scrollbars) | `CssBaseline` overrides or `GlobalStyles` hoisted to a constant | Component files |
| Page layout | `Grid` (`size` prop), `Stack`, `Container`, `Box` with `sx` | Hand-written flex CSS per page |
| Large tables: server-side paging, sorting, filtering | MUI X Data Grid (`DataGrid` is MIT; Pro and Premium need a licence key) | A hand-built `Table` with client-side sorting over thousands of rows |

## Rules

| Area | Rule |
|---|---|
| Tokens | Read colours from the theme: `theme.vars.palette.primary.main` in `styled` and `sx` callbacks, palette paths in `sx` (`'primary.main'`). No hex values, px font sizes or magic spacing in components. A new token goes under `colorSchemes.<scheme>.palette`, logged as `DECIDE`. |
| Dark mode | Style dark variants with `theme.applyStyles('dark', { … })`. Never branch on `theme.palette.mode`: it flickers on SSR. |
| Selectors | Target the stable classes `.Mui<Component>-<slot>`; pair state classes with a component class (`.MuiOutlinedInput-root.Mui-error`). Never hashed `css-…` classes. |
| Imports | Path imports: `import Button from '@mui/material/Button'`, `import DeleteIcon from '@mui/icons-material/Delete'`. Barrel imports slow dev builds, icons by up to 6×. In Next.js, `optimizePackageImports` is the alternative. |
| Next.js App Router | Wrap `<body>` children in `AppRouterCacheProvider` from `@mui/material-nextjs/v<next major>-appRouter`, then `ThemeProvider` and `CssBaseline`. MUI components are client components: keep them in `'use client'` leaves; the theme file is `'use client'`. |
| Next.js links | A house `Link` that passes `next/link` to MUI's `component` prop. On Next.js 16, wrap `next/link` in a `'use client'` component first ("Functions cannot be passed directly to Client Components"). |
| Forms | `TextField` with `label`, `helperText` and `error` from the form library (React Hook Form + `Controller`, or Formik). Map API field errors to `error` + `helperText`. Disable the submit `Button` while pending. |
| Accessibility | Every `TextField` has a `label`; every `IconButton` has an `aria-label`; `Dialog` gets `aria-labelledby` pointing at `DialogTitle`'s id; keep `focusVisible` styles |
| Dialogs and menus | Close through `onClose(event, reason)`; check `reason` (`'escapeKeyDown'`, `'backdropClick'`) instead of removed props |
| Data Grid | Server mode for real data: `paginationMode`, `sortingMode` and `filterMode` set to `'server'`, `rowCount` from the API. Stable `columns` (define outside the component or `useMemo`). |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | Vitest or Jest on pure modules (formatters, schemas, mappers, theme helpers) | No DOM, no network. List slow tests with the runner's reporter (`vitest --reporter=verbose`, `jest --verbose`). |
| Medium | Testing Library (`@testing-library/react`, `user-event`) rendering inside the app's `ThemeProvider`; MSW for the API | Query by role and label (`getByRole('combobox')` for Autocomplete and Select, `getByRole('dialog')`). Dialogs, menus and popovers portal to `document.body`: query `screen`, not the render container. |
| Large | Playwright or Cypress against the built app and the real API | Stub only external systems at the network edge. Role and label locators, never `.MuiButton-root`. |

Snapshot tests are out (testing.md). In v9 MUI no longer checks `NODE_ENV === 'test'`, so DOM details can differ from v7 in tests.

## Performance

| Rule | How |
|---|---|
| Dev builds | Path imports, or `optimizePackageImports: ['@mui/material', '@mui/icons-material']` in Next.js |
| Styles at runtime | Prefer theme `styleOverrides` and `styled()` for hot lists; heavy dynamic `sx` objects in long lists recompute on every render |
| Long lists and tables | MUI X Data Grid virtualises rows; for custom lists, virtualise (`react-window`) beyond a few hundred rows |
| Re-renders | Memoise only to fix a measured problem (React DevTools Profiler) |

## Review checklist

| Finding | Sev |
|---|---|
| An input without a label, an `IconButton` without `aria-label`, a `Dialog` without `aria-labelledby` | `must` |
| A removed v9 API (`GridLegacy`, system props, `InputProps`, `PaperProps`, `components`, `disableEscapeKeyDown`) in new code | `must` on v9, `should` on v7 |
| A hex colour, px font size or `theme.palette.mode` branch in a component | `should` |
| A barrel import from `@mui/icons-material` | `should` |
| A selector on a hashed `css-…` class, or a bare state class (`.Mui-disabled`) | `should` |
| A client-side sorted `Table` over a server-paged dataset | `should` |

## Sources

Indexed in `references/sources.md`: Material UI v9 docs (theming, CSS variables, customization, Next.js integration, migration guides), MUI X Data Grid, and the testing tools above.
