# Sources: React + Material UI

Check `@mui/material` in `package.json` first. `mui.com` serves the latest major; older majors live at `v7.mui.com`, `v6.mui.com`.
Where a source conflicts with this pack's SKILL.md, the pack wins: it is the house style.

## Versions and migration

| Source | URL | Use it for |
|---|---|---|
| Upgrade to v9 | https://mui.com/material-ui/migration/upgrade-to-v9/ | Every removed prop and behaviour change from v7, with codemods |
| Upgrade to v7 | https://mui.com/material-ui/migration/upgrade-to-v7/ | Coming from v6: package layout, Grid rename, deprecations |
| Material UI v9 release post | https://mui.com/blog/introducing-material-ui-v9/ | What v9 adds: NumberField, Menubar, CSS variables, keyboard fixes |
| Material UI and MUI X v9 | https://mui.com/blog/introducing-mui-v9/ | Shared major across Material UI and MUI X; licensing changes |
| Versions | https://mui.com/versions/ | Which major is current, links to older docs |

## Theming and styling

| Source | URL | Use it for |
|---|---|---|
| How to customize | https://mui.com/material-ui/customization/how-to-customize/ | The ladder: `sx` → `styled()` → theme overrides → global CSS; stable class names and state classes |
| Theming | https://mui.com/material-ui/customization/theming/ | `createTheme`, `ThemeProvider`, nesting, custom variables |
| Themed components | https://mui.com/material-ui/customization/theme-components/ | `defaultProps`, `styleOverrides`, `variants` per component |
| CSS theme variables: usage | https://mui.com/material-ui/customization/css-theme-variables/usage/ | `cssVariables: true`, `colorSchemes`, `theme.vars`, `theme.applyStyles` |
| CSS theme variables: configuration | https://mui.com/material-ui/customization/css-theme-variables/configuration/ | Toggling schemes, `InitColorSchemeScript`, SSR flicker |
| Dark mode | https://mui.com/material-ui/customization/dark-mode/ | Light and dark schemes, `useColorScheme` |
| The `sx` prop | https://mui.com/system/getting-started/the-sx-prop/ | Theme-aware shorthands, callbacks, nested selectors |
| `styled()` | https://mui.com/system/styled/ | Reusable styled components, `shouldForwardProp` |
| CSS layers | https://mui.com/material-ui/customization/css-layers/ | Coexisting with Tailwind or other CSS through `@layer mui` |

## Components and layout

| Source | URL | Use it for |
|---|---|---|
| Grid | https://mui.com/material-ui/react-grid/ | `size`, `offset`, nested grids |
| Text Field | https://mui.com/material-ui/react-text-field/ | Labels, helper text, errors, `slotProps` |
| Autocomplete | https://mui.com/material-ui/react-autocomplete/ | Async options, free solo, accessibility |
| Dialog | https://mui.com/material-ui/react-dialog/ | `onClose` reasons, `aria-labelledby`, full-screen dialogs |
| MUI X Data Grid | https://mui.com/x/react-data-grid/ | Server-side pagination, sorting and filtering; editing; licensing tiers |

## Integrations and performance

| Source | URL | Use it for |
|---|---|---|
| Next.js integration | https://mui.com/material-ui/guides/nextjs | `AppRouterCacheProvider`, `next/font`, Pages Router setup |
| Minimizing bundle size | https://mui.com/guides/minimizing-bundle-size/ | Path imports, the `path-imports` codemod, ESLint rule |

## Testing

| Source | URL | Use it for |
|---|---|---|
| Testing Library: guiding principles | https://testing-library.com/docs/guiding-principles | Test what the user sees, not implementation |
| Testing Library: query priority | https://testing-library.com/docs/queries/about/#priority | `getByRole` > `getByLabelText` > … > test id |
| user-event | https://testing-library.com/docs/user-event/intro | Realistic typing, clicking and keyboard navigation |
| Vitest | https://vitest.dev/guide/ | Unit and component runner |
| MSW | https://mswjs.io/docs/ | Mocking the API at the network level |
| Playwright best practices | https://playwright.dev/docs/best-practices | Isolation, locators, web-first assertions |
