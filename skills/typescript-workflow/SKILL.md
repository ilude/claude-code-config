---
name: typescript-workflow
description: TypeScript/JavaScript project workflow guidelines using Bun package manager. Covers bun run, bun install, bun add, tsconfig.json patterns, ESM/CommonJS modules, type safety, Prettier/ESLint/Biome formatting, naming conventions (PascalCase, camelCase, UPPER_SNAKE_CASE), project structure, error handling, environment variables, async patterns, and code quality tools. Activate when working with TypeScript files (.ts, .tsx), JavaScript files (.js, .jsx), Bun projects, tsconfig.json, package.json, bun.lock, or Bun-specific tooling.
---

# TypeScript/JavaScript Projects Workflow

Guidelines for working with TypeScript and JavaScript projects using Bun as the primary package manager with modern tooling and best practices.

## CRITICAL: Bun Package Manager

**ALWAYS use Bun commands** for all package and runtime operations in Bun projects:

```bash
# Package management
bun install        # Install dependencies from package.json
bun add <package>  # Add production dependency
bun add --dev <package>  # Add development dependency
bun remove <package>  # Remove dependency

# Running code and scripts
bun run <script>   # Run script defined in package.json
bun <file.ts>      # Run TypeScript/JavaScript directly
bun run build      # Run build script

# Testing
bun test           # Run tests with Bun's native test runner

# Package info
bun list           # List installed packages
bun outdated       # Check for updates
```

**Benefits of Bun:**
- Native TypeScript support (no transpilation setup)
- Significantly faster than Node.js
- All-in-one tool (package manager, runtime, test runner)
- Smaller node_modules footprint
- Drop-in Node.js compatibility for most packages

## Module Systems

### ESM (ECMAScript Modules) - Preferred

**Default for Bun projects and modern TypeScript:**

```typescript
// Import named exports
import { UserService } from './services/user-service';
import { type User } from './types';

// Import default exports
import express from 'express';

// Import with alias
import * as helpers from './utils/helpers';

// Export named
export function getUserById(id: string): Promise<User> {
  // ...
}

// Export default
export default UserService;

// Re-export
export { type User } from './types';
export { UserService } from './services/user-service';
```

### CommonJS Fallback

Use only when necessary for legacy compatibility:

```javascript
// Require imports
const { UserService } = require('./services/user-service');
const express = require('express');

// Module exports
module.exports = UserService;
module.exports = { UserService, UserRepository };
```

### Mixed Module Usage

In `package.json`, specify module type:

```json
{
  "type": "module",
  "name": "my-app",
  "version": "1.0.0"
}
```

## TypeScript Configuration

### tsconfig.json Best Practices

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020"],
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "allowJs": false,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@services/*": ["src/services/*"],
      "@models/*": ["src/models/*"]
    },
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Key Options Explained

- **target:** ES2020 for modern environments, ES2015 for legacy support
- **module:** ESNext for Bun/bundlers, CommonJS for Node.js compatibility
- **moduleResolution:** bundler (for Bun/bundlers), node (for Node.js)
- **strict:** Enable all strict type checking
- **skipLibCheck:** Skip type checking of declaration files
- **baseUrl + paths:** Enable path aliases for cleaner imports
- **noUnusedLocals/Parameters:** Catch dead code

## Code Style and Formatting

### Prettier Configuration

Standard Prettier setup for consistent formatting:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

### ESLint Configuration

```javascript
export default [
  {
    ignores: ['node_modules', 'dist', 'build', '*.config.js'],
  },
  {
    files: ['src/**/*.{ts,tsx,js,jsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',
        process: 'readonly',
      },
    },
    rules: {
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-unused-vars': 'off',
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },
];
```

### Biome (Alternative All-in-One)

Modern alternative combining linting and formatting:

```json
{
  "organizeImports": {
    "enabled": true
  },
  "formatter": {
    "enabled": true,
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

Run with: `biome check --apply src/`

### Running Formatters

```bash
# Prettier
bun add --dev prettier
bun run prettier --write src/

# ESLint
bun add --dev eslint
bun run eslint src/ --fix

# Biome
bun add --dev @biomejs/biome
bun run biome check --apply src/
```

## Naming Conventions

### File Naming

- **Components:** PascalCase - `UserProfile.tsx`, `LoginForm.tsx`
- **Utilities/Helpers:** camelCase - `formatDate.ts`, `apiClient.ts`
- **Types/Interfaces:** PascalCase - `User.ts`, `ApiResponse.ts`
- **Constants:** UPPER_SNAKE_CASE - `API_ENDPOINTS.ts`, `CONFIG.ts`
- **Test files:** `.test.ts` or `.spec.ts` suffix - `user.service.test.ts`

### Code Naming

```typescript
// Classes and Types: PascalCase
class UserService {
  // Methods and properties: camelCase
  getUserById(id: string): Promise<User> {
    // Local variables: camelCase
    const userData = {};
    return userData;
  }

  // Private members: camelCase with leading underscore
  private _cache: Map<string, User> = new Map();
  private _validateUser(user: User): boolean {
    return true;
  }
}

// Interfaces: PascalCase (sometimes with I prefix, but discouraged)
interface UserRepository {
  getById(id: string): Promise<User | null>;
}

// Enums: PascalCase
enum UserRole {
  Admin = 'ADMIN',
  User = 'USER',
  Guest = 'GUEST',
}

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;
const DEFAULT_TIMEOUT = 5000;
const API_BASE_URL = 'https://api.example.com';

// Variables and functions: camelCase
let retryCount = 0;
function getUserData(id: string) {
  // ...
}
```

### React Component Naming

```typescript
// Component files: PascalCase
export function UserProfile({ userId }: { userId: string }) {
  // Props interface: PascalCase with Props suffix
  return <div>Profile</div>;
}

// Hook files: camelCase with use prefix
export function useUserData(userId: string) {
  // ...
}

// Context: PascalCase
const UserContext = createContext<User | null>(null);

export function UserProvider({ children }: { children: React.ReactNode }) {
  return <UserContext.Provider value={null}>{children}</UserContext.Provider>;
}
```

## Type Safety and Annotations

### Type Hints

- **Explicit types** for function parameters and return values
- **Never use `any`** - use `unknown` and type narrowing if needed
- **Avoid implicit `any`** - enable `noImplicitAny` in tsconfig.json

```typescript
// Function parameters and return types
function processUser(user: User): Promise<ProcessedUser> {
  // ...
}

// Arrow functions
const formatName = (first: string, last: string): string => {
  return `${first} ${last}`;
};

// Complex types
type ApiResponse<T> = {
  status: number;
  data: T;
  error?: string;
};

interface RequestHandler {
  handle(request: Request): Promise<Response>;
}
```

### Generics

```typescript
// Generic functions
function getById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find((item) => item.id === id);
}

// Generic classes
class Repository<T> {
  async getById(id: string): Promise<T | null> {
    // ...
  }
}

// Generic types
type Result<T, E = Error> = { success: true; data: T } | { success: false; error: E };
```

### Data Validation

Use **Zod** for runtime validation with type inference:

```typescript
import { z } from 'zod';

// Schema definition
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// Type inference from schema
type User = z.infer<typeof UserSchema>;

// Runtime validation
function createUser(data: unknown): User {
  return UserSchema.parse(data);
}

// Safe parsing with error handling
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.error(result.error.format());
}
```

## Project Structure

### Recommended Directory Layout

```
project/
├── src/
│   ├── main.ts              # Entry point
│   ├── index.ts             # Main exports
│   ├── types/               # Type definitions
│   │   ├── user.ts
│   │   ├── api.ts
│   │   └── index.ts
│   ├── services/            # Business logic services
│   │   ├── user-service.ts
│   │   └── auth-service.ts
│   ├── repositories/        # Data access layer
│   │   ├── user-repository.ts
│   │   └── base-repository.ts
│   ├── models/              # Data models
│   │   ├── user.ts
│   │   └── product.ts
│   ├── handlers/            # Request/event handlers
│   │   ├── user-handler.ts
│   │   └── auth-handler.ts
│   ├── middleware/          # Express/web middleware
│   │   ├── auth-middleware.ts
│   │   └── error-middleware.ts
│   ├── utils/               # Utility functions
│   │   ├── logger.ts
│   │   ├── formatters.ts
│   │   └── validators.ts
│   └── config/              # Configuration
│       ├── env.ts
│       └── constants.ts
├── tests/
│   ├── unit/
│   │   └── services/
│   ├── integration/
│   └── fixtures/
├── dist/                    # Compiled output (gitignored)
├── .github/
│   └── workflows/           # CI/CD workflows
├── package.json
├── tsconfig.json
├── prettier.config.js
├── eslint.config.js
├── biome.json
├── bun.lock
├── .gitignore
└── README.md
```

### Import Patterns

```typescript
// Absolute imports with path aliases
import { UserService } from '@services/user-service';
import type { User } from '@models/user';

// Relative imports within same feature
import { UserRepository } from '../repositories/user-repository';
import { validateUser } from '../utils/validators';

// Re-exports from index files
export { UserService, UserRepository } from './index';
```

## Error Handling

### Exception Best Practices

```typescript
// Define custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class ValidationError extends AppError {
  constructor(message: string, public field: string) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

// Type-safe error handling
async function getUser(id: string): Promise<User> {
  if (!id || id.trim() === '') {
    throw new ValidationError('User ID cannot be empty', 'id');
  }

  try {
    const user = await database.users.findById(id);
    if (!user) {
      throw new NotFoundError(`User ${id} not found`);
    }
    return user;
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }
    throw new AppError('Failed to fetch user', 'DATABASE_ERROR', 500);
  }
}

// Result pattern for explicit error handling
type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeFetchUser(id: string): Promise<Result<User, AppError>> {
  try {
    const user = await getUser(id);
    return { ok: true, value: user };
  } catch (error) {
    return { ok: false, error: error instanceof AppError ? error : new AppError('Unknown error', 'UNKNOWN', 500) };
  }
}
```

## Configuration Management

### Environment Variables

Use **dotenv** for development and environment validation:

```bash
bun add dotenv
bun add --dev @types/node
```

```typescript
// env.ts
import { z } from 'zod';

// Define schema
const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string(),
  DEBUG: z.enum(['true', 'false']).transform((v) => v === 'true').default('false'),
});

// Parse and validate
const env = EnvSchema.parse(process.env);

export default env;
```

Usage:

```typescript
import env from './config/env';

console.log(env.PORT);        // 3000
console.log(env.DATABASE_URL); // https://...
console.log(env.DEBUG);        // false
```

### Configuration Files

Organize settings by environment:

```typescript
// config/database.ts
import env from './env';

const databaseConfigs = {
  development: {
    host: 'localhost',
    port: 5432,
    database: 'myapp_dev',
  },
  production: {
    host: env.DATABASE_HOST,
    port: 5432,
    database: env.DATABASE_NAME,
  },
};

export const dbConfig = databaseConfigs[env.NODE_ENV];
```

## Common Async Patterns

### Async/Await

```typescript
// Basic async function
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch');
    return response.json();
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}

// Calling async functions
const user = await fetchUserData('123');

// Sequential operations
async function createUserProfile(userId: string, profileData: unknown): Promise<void> {
  const user = await getUser(userId);
  const profile = await createProfile(user.id, profileData);
  await linkProfileToUser(user.id, profile.id);
}

// Concurrent operations
async function loadDashboardData(): Promise<DashboardData> {
  const [users, products, stats] = await Promise.all([
    fetchUsers(),
    fetchProducts(),
    fetchStats(),
  ]);
  return { users, products, stats };
}
```

### Promise Chains (When Needed)

```typescript
function fetchUserChain(id: string): Promise<User> {
  return fetch(`/api/users/${id}`)
    .then((res) => {
      if (!res.ok) throw new Error('Not found');
      return res.json();
    })
    .then((user) => validateUser(user))
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
}
```

### Error Handling in Async Code

```typescript
// Try-catch pattern
async function safeOperation(): Promise<void> {
  try {
    const result = await riskyOperation();
    console.log(result);
  } catch (error) {
    if (error instanceof ValidationError) {
      console.log('Validation failed:', error.message);
    } else {
      console.log('Unexpected error:', error);
    }
  } finally {
    cleanup();
  }
}

// Promise.catch pattern
function chainedOperation(): Promise<void> {
  return riskyOperation()
    .then((result) => processResult(result))
    .catch((error) => handleError(error))
    .finally(() => cleanup());
}
```

## Testing Integration

### Test Setup with Bun

```bash
bun add --dev @testing-library/react @testing-library/jest-dom
```

See **typescript-testing** skill for comprehensive testing patterns.

### Example Tests

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'bun:test';
import { UserService } from '@services/user-service';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  it('should fetch user by id', async () => {
    const user = await service.getById('123');
    expect(user).toBeDefined();
    expect(user?.id).toBe('123');
  });

  it('should throw NotFoundError for non-existent user', async () => {
    expect(async () => {
      await service.getById('nonexistent');
    }).toThrow();
  });
});
```

## Quick Reference

**Bun Commands:**
- `bun install` - Install dependencies
- `bun add <pkg>` - Add production dependency
- `bun add --dev <pkg>` - Add dev dependency
- `bun run <script>` - Run package.json script
- `bun <file.ts>` - Execute TypeScript directly
- `bun test` - Run tests

**Key Rules:**
- Always use Bun commands in Bun projects
- Use ESM (import/export) by default
- Enable strict TypeScript (`"strict": true`)
- Use path aliases for cleaner imports
- Validate all external input with Zod or similar
- Use custom error classes for errors
- Use `async/await` for asynchronous code
- Define types at module level, use constants for values
- Never use `any` - use `unknown` and type guards
- Use result types or custom errors for error handling

**Tools:**
- **Prettier:** Code formatting
- **ESLint:** Linting and best practices
- **Biome:** All-in-one alternative
- **Zod:** Runtime validation with type inference
- **Bun Test:** Native test runner

---

**Note:** For project-specific TypeScript patterns, check `.claude/CLAUDE.md` in the project directory.
