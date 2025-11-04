---
name: web-projects
description: Guidelines for web development projects using JavaScript/TypeScript frameworks. Activate when working with web projects, package.json, npm/yarn/pnpm, React, Next.js, Vue, Angular, Svelte, or other web frameworks, frontend components, or Node.js applications.
---

# Web Projects

Guidelines for working with web development projects using modern JavaScript/TypeScript frameworks.

## Project Structure Recognition

### Package Managers
- Check `package.json` for dependencies and scripts
- Identify package manager: npm, yarn, or pnpm
- Look for lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`

### Framework Detection
Look for framework-specific configuration files:
- **Next.js**: `next.config.js`, `next.config.ts`
- **Vite**: `vite.config.js`, `vite.config.ts`
- **React**: Check `package.json` dependencies
- **Vue**: `vue.config.js`, `vite.config.ts` with Vue plugin
- **Angular**: `angular.json`
- **Svelte**: `svelte.config.js`

## Development Workflow

### Package Manager Usage
Respect the project's chosen package manager:
- **npm**: `npm install`, `npm run`, `npm test`
- **yarn**: `yarn install`, `yarn`, `yarn test`
- **pnpm**: `pnpm install`, `pnpm run`, `pnpm test`

**Detection:**
- Presence of lock file indicates preferred package manager
- `.npmrc`, `.yarnrc`, or `pnpm-workspace.yaml` configs

### Common Scripts
Check `package.json` "scripts" section for:
- `dev` or `start` - Development server
- `build` - Production build
- `test` - Run tests
- `lint` - Linting
- `format` - Code formatting

## Code Patterns

### Component Patterns
- **Respect existing patterns** - Don't change established component structure
- Check for component naming conventions
- Look for existing patterns in components directory
- Follow established import/export patterns

### Testing Setup
- **Respect existing test framework** - Jest, Vitest, Testing Library, Cypress, Playwright
- Check test configuration in `package.json` or dedicated config files
- Look for existing test patterns
- Follow established test file naming (`.test.js`, `.spec.ts`, etc.)

### Styling Approach
Identify and follow the project's styling method:
- CSS Modules (`.module.css`)
- Styled Components / Emotion
- Tailwind CSS (`tailwind.config.js`)
- SASS/SCSS (`.scss` files)
- Plain CSS

## Configuration Files

### Common Config Files
- `tsconfig.json` - TypeScript configuration
- `.eslintrc` - Linting rules
- `.prettierrc` - Code formatting
- `jest.config.js` or `vitest.config.ts` - Test configuration
- `.env.local`, `.env.development` - Environment variables

## Quick Reference

**Before making changes:**
- ✅ Check `package.json` for scripts and dependencies
- ✅ Identify package manager from lock file
- ✅ Review existing component patterns
- ✅ Check framework-specific configurations

**Development:**
- Use project's package manager consistently
- Follow existing code organization
- Respect established patterns and conventions
- Check test setup before writing tests

**Common mistakes to avoid:**
- ❌ Mixing package managers
- ❌ Ignoring existing component patterns
- ❌ Using different styling approach than project
- ❌ Changing test framework without discussion

---

**Note:** Web projects vary greatly - always check the project's specific configuration and patterns before making assumptions.
