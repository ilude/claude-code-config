---
name: api-design-patterns
description: Language-agnostic API design patterns covering REST and GraphQL, including resource naming, HTTP methods, status codes, versioning, pagination, filtering, authentication, error handling, and schema design. Activate when working with APIs, REST endpoints, GraphQL schemas, API documentation, OpenAPI/Swagger, JWT, OAuth2, endpoint design, API versioning, rate limiting, or GraphQL resolvers.
---

# API Design Patterns

Language-agnostic patterns for designing robust, scalable REST and GraphQL APIs. Focus on solving real problems with simple, maintainable solutions.

**Auto-activate when:** Working with API routes, endpoints, REST design, GraphQL schemas, OpenAPI/Swagger specs, authentication tokens, API documentation, or discussing endpoint design, versioning strategies, or API architecture.

## Philosophy

- **Simple over clever** - Choose straightforward patterns that solve the problem
- **Consistency** - Apply patterns consistently across endpoints
- **Pragmatism** - Pick approaches based on actual use cases, not theoretical purity
- **No over-engineering** - Don't add features or complexity "just in case"

---

## REST API Design

### Resource Naming Conventions

**Principles:**
- Use **nouns** for resource names, not verbs
- Use **lowercase** with hyphens for multi-word resources
- Represent relationships hierarchically
- Use **plural** for collections

```
✅ Good patterns:
GET  /users
GET  /users/{id}
GET  /users/{id}/posts
GET  /users/{id}/posts/{post_id}/comments
POST /users
PUT  /users/{id}
DELETE /users/{id}

❌ Avoid verbs:
GET /getUsers
GET /fetchUserById
POST /createUser
GET /getUserPosts
```

**Special cases:**
- **Singular for singleton resources:** `/profile`, `/settings` (user-specific, not collections)
- **Actions as sub-resources:** `/users/{id}/activate` (when GET/POST semantics don't fit)
- **Search/filter:** Use query parameters, not new endpoints
  - `GET /users?role=admin&status=active`
  - NOT `GET /users/admins` or `GET /active-users`

### HTTP Methods

| Method | Purpose | Idempotent | Safe | Has Body |
|--------|---------|-----------|------|----------|
| **GET** | Retrieve resource | Yes | Yes | No |
| **POST** | Create new resource | No | No | Yes |
| **PUT** | Replace entire resource | Yes | No | Yes |
| **PATCH** | Partial update | No | No | Yes |
| **DELETE** | Remove resource | Yes | No | No |
| **HEAD** | Like GET, no body | Yes | Yes | No |
| **OPTIONS** | Describe communication | Yes | Yes | No |

**Best practices:**
- **GET** - Never for mutations; safe to retry
- **POST** - Create new or trigger actions; use 201 Created
- **PUT** - Full replacement; include all fields
- **PATCH** - Partial update; only changed fields
- **DELETE** - Use 204 No Content or 200 with body

**Avoid:** PATCH if API is simple; use PUT instead. Don't mix PUT/PATCH semantics.

### HTTP Status Codes

**2xx Success:**
- `200 OK` - General success (GET, PUT with response body)
- `201 Created` - Resource created (POST)
- `204 No Content` - Success, no body (DELETE, PATCH with no response)
- `202 Accepted` - Request queued, will process asynchronously

**3xx Redirection:**
- `301 Moved Permanently` - Resource moved (deprecated endpoints)
- `304 Not Modified` - Client cache valid (use ETag/If-None-Match)

**4xx Client Error:**
- `400 Bad Request` - Invalid input (malformed JSON, missing fields)
- `401 Unauthorized` - Missing or invalid auth
- `403 Forbidden` - Authenticated but no permission
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Concurrent update or constraint violation
- `422 Unprocessable Entity` - Semantically invalid (validation errors)
- `429 Too Many Requests` - Rate limit exceeded

**5xx Server Error:**
- `500 Internal Server Error` - Unexpected error
- `503 Service Unavailable` - Temporary downtime

### Versioning Strategies

**Option 1: URL Path (Explicit, Straightforward)**
```
/api/v1/users
/api/v2/users
```
Pros: Clear, cacheable, explicit breaking changes
Cons: Multiple code paths, redundancy

**Option 2: Header-based (Clean URLs)**
```
GET /api/users
Accept-Version: 1.0
```
Pros: Clean URLs, version handling logic centralized
Cons: Less obvious in browser/logs

**Option 3: Media Type (Accept header)**
```
GET /api/users
Accept: application/vnd.myapi.v2+json
```
Pros: RESTful, content negotiation
Cons: Complex, less common

**Recommendation:** Use URL versioning for major changes. Avoid if possible - design for **forward compatibility**:
- Add fields without removing old ones
- Make new features optional
- Deprecated endpoints return 410 Gone with migration info

### Pagination Patterns

**Offset/Limit (Simple, works for small datasets):**
```json
GET /users?offset=0&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "total": 1500
  }
}
```

**Cursor-based (Scalable, efficient for large datasets):**
```json
GET /users?cursor=abc123&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "cursor": "next_cursor_xyz",
    "limit": 20
  }
}
```
Pros: Efficient queries, works with distributed systems
Cons: Cursor generation logic needed

**Keyset pagination (Efficient, uses natural ordering):**
```
GET /users?after_id=123&limit=20
```
Use natural sort fields (ID, timestamp) instead of arbitrary cursors.

**Recommendation:**
- Small fixed datasets: offset/limit
- Large or growing datasets: cursor-based
- Simple endpoints: keyset pagination

### Filtering, Sorting, Searching

**Filtering:**
```
GET /users?role=admin&status=active&department=sales
GET /posts?created_after=2024-01-01&created_before=2024-12-31
```

**Sorting:**
```
GET /users?sort=name,-created_at
(hyphen = descending)

Or explicit:
GET /users?sort_by=name&sort_order=asc
```

**Searching:**
```
GET /users?search=john
GET /posts?q=api+design

(Full-text search, implementation-specific)
```

**Validation:**
- Whitelist allowed filter/sort fields
- Escape search queries (SQL injection prevention)
- Limit result count with pagination

### Rate Limiting

**Headers:**
```
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1629801600
```

**When limit exceeded:**
```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

**Strategies:**
- **Token bucket** - Smooth bursts, standard
- **Leaky bucket** - Even distribution
- **Fixed window** - Simple, vulnerable to boundary abuse
- **Sliding window** - Balanced complexity/accuracy

**Recommendation:** Token bucket per user/API key with reasonable defaults (e.g., 1000 req/hour).

---

## Request/Response Patterns

### Request Validation

**Validate early:**
```
1. Schema validation (required fields, types)
2. Format validation (email, UUID, dates)
3. Business logic validation (duplicate check, range)
4. Return appropriate error
```

**Request validation example:**
```json
POST /users
{
  "email": "user@example.com",
  "name": "John Doe",
  "age": 30
}
```

**Validation error response (400/422):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_EMAIL",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Age must be >= 18"
      }
    ]
  }
}
```

### Error Response Format

**Consistent error structure:**
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with id 123 does not exist",
    "status": 404,
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

Or simplified for simple APIs:
```json
{
  "code": "INVALID_REQUEST",
  "message": "Missing required field: email"
}
```

**Error codes (use consistently):**
- `INVALID_REQUEST` - Malformed request
- `VALIDATION_ERROR` - Field validation failed
- `AUTHENTICATION_FAILED` - Invalid credentials
- `INSUFFICIENT_PERMISSIONS` - Authorized but lacks permission
- `RESOURCE_NOT_FOUND` - 404
- `RESOURCE_ALREADY_EXISTS` - 409 on duplicate
- `INTERNAL_SERVER_ERROR` - 500

### Success Response Format

**Envelope pattern (good for APIs with metadata):**
```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

**Direct pattern (simpler, common in modern APIs):**
```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Collection response:**
```json
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "pagination": {
    "cursor": "next_page",
    "limit": 20
  }
}
```

**Recommendation:** Keep responses consistent. Use envelopes if you need pagination/meta at root level. For collections, include pagination separately.

### Partial Responses (Optional)

Allow clients to request specific fields:
```
GET /users/123?fields=id,name,email
```

Reduces bandwidth for large objects. Implement via field selection in queries (GraphQL does this naturally).

---

## Authentication & Authorization

### API Key Pattern

**Simple, good for service-to-service:**
```
GET /api/data
Authorization: Bearer api_key_xyz

or

GET /api/data?api_key=xyz123
```

**Pros:** Simple, easy to debug
**Cons:** Less secure than OAuth2, no scoping

**Storage:** Use secure vaults, never log keys, rotate regularly.

### JWT (JSON Web Token)

**Flow:**
```
1. Client authenticates (POST /auth/login)
2. Server returns JWT
3. Client includes in Authorization header
4. Server validates signature

GET /api/protected
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**JWT structure:** `header.payload.signature`
```json
Header: { "alg": "HS256", "typ": "JWT" }
Payload: { "sub": "user123", "exp": 1629801600, "scope": "read write" }
Signature: HMACSHA256(header.payload, secret)
```

**Best practices:**
- Store secret securely (environment variable, vault)
- Include expiration (`exp`)
- Use HTTPS only
- Validate signature on every request
- Refresh tokens for long-lived sessions
- Include scopes for fine-grained permissions

### OAuth2 (Delegated Authorization)

**Flow (Authorization Code):**
```
1. User clicks "Login with Google"
2. Redirect to OAuth provider
3. User authenticates with provider
4. Provider redirects back with auth code
5. Server exchanges code for access token
6. Server gets user info, creates session
```

**When to use:** Third-party integrations, user account delegation

**Scopes:**
```
scope=read write user:email profile
```

### Permission Models

**Role-based (RBAC):**
```
User → Role(s) → Permission(s)

admin: can do everything
moderator: can delete comments, ban users
user: can create posts, read public data
```

**Attribute-based (ABAC):**
```
Can user perform action on resource?

Policy: user can delete post if:
  - user.role == "admin" OR
  - resource.owner_id == user.id OR
  - user.created_at < resource.created_at - 24hours
```

**Recommendation:** Start with RBAC (simpler). Move to ABAC only if needed.

**Implementation:**
```
Middleware approach:
1. Extract user/token from request
2. Load user permissions
3. Check against required permission
4. Allow/deny
```

---

## GraphQL Patterns

### Schema Design

**Build around data needs, not database structure:**
```graphql
# ✅ Good: Organized by domain
type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
  followers(first: Int): UserConnection!
}

type Post {
  id: ID!
  title: String!
  body: String!
  author: User!
  comments(first: Int): CommentConnection!
  publishedAt: DateTime!
}

# ❌ Avoid: Exposing raw database structure
type UserRow {
  user_id: Int!
  user_name: String!
  created_timestamp: String!
}
```

**Nullability:**
```graphql
# Sensible defaults
type User {
  id: ID!             # Always required
  email: String!      # Required
  bio: String         # Optional, may be null
  posts: [Post!]!     # Required array, posts required
}
```

### Query vs Mutation

**Queries:** Read operations, always safe to execute multiple times
```graphql
query {
  user(id: "123") {
    name
    email
    posts { title }
  }
}
```

**Mutations:** Write operations, may have side effects
```graphql
mutation {
  createPost(input: {title: "...", body: "..."}) {
    id
    createdAt
  }
}
```

**Batch operations:**
```graphql
mutation {
  updateUsers(updates: [{id: "1", name: "Alice"}, {id: "2", name: "Bob"}]) {
    id
    name
  }
}
```

### Resolvers

**Resolver anatomy:**
```
function resolve(parent, args, context, info) {
  // parent: object containing this field
  // args: arguments passed to field
  // context: shared data (user, db, etc)
  // info: field metadata
  return data
}
```

**Example:**
```javascript
const resolvers = {
  Query: {
    user: (parent, { id }, context) => {
      return context.userDB.findById(id);
    }
  },
  User: {
    posts: (user, { first }, context) => {
      return context.postDB.findByAuthorId(user.id).limit(first);
    }
  }
};
```

**Key principle:** Resolvers should be simple, push logic to services/repositories.

### N+1 Query Problem

**Problem:**
```
User query returns 100 users
For each user, resolve posts (100 queries!)
Total: 1 + 100 = 101 queries
```

**Solution 1: DataLoader (Batching)**
```javascript
const userLoader = new DataLoader(async (userIds) => {
  // Load all users at once instead of individually
  return database.users.findByIds(userIds);
});

// In resolver:
User: {
  posts: (user, args, context) => {
    // Uses batched loader
    return context.postLoader.loadByAuthorId(user.id);
  }
}
```

**Solution 2: Proactive Loading**
```javascript
Query: {
  users: async (parent, args, context) => {
    const users = await context.userDB.find();
    // Batch load all posts for users
    const postMap = await context.postDB.findByAuthorIds(
      users.map(u => u.id)
    );
    users.forEach(u => u._postsMap = postMap[u.id]);
    return users;
  }
}
```

**Recommendation:** Use DataLoader for most cases. Simple and effective.

### Error Handling

**GraphQL errors:**
```json
{
  "data": {
    "user": null
  },
  "errors": [
    {
      "message": "User not found",
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND",
        "status": 404
      }
    }
  ]
}
```

**Pattern:** Partial data + errors in extensions. Allows graceful degradation.

---

## API Documentation

### OpenAPI/Swagger

**Minimal example:**
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: User list
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id: { type: string }
        name: { type: string }
        email: { type: string }
      required: [id, name, email]
```

**Tools:**
- Swagger UI - Interactive exploration
- ReDoc - Clean documentation
- Postman - API client and testing

### GraphQL Schema Documentation

**Introspection (built-in):**
```graphql
{
  __schema {
    types {
      name
      description
      fields { name, description, type }
    }
  }
}
```

**Tools:**
- GraphQL Playground - Interactive IDE
- GraphQL Explorer (Apollo) - Documented explorer
- Voyager - Schema visualization

**Write descriptive type/field definitions:**
```graphql
"""
User account in the system.
Each user has a unique email and can create multiple posts.
"""
type User {
  """Unique identifier (UUID)"""
  id: ID!

  """User's full name"""
  name: String!

  """Email address (must be unique)"""
  email: String!
}
```

---

## Common Pitfalls & Solutions

### Pitfall: Endpoint Explosion

**Problem:** Creating endpoints for every slight variation
```
GET /users
GET /users/admins
GET /users/active
GET /users/verified
```

**Solution:** Use filtering
```
GET /users?role=admin&status=active&verified=true
```

### Pitfall: Inconsistent Error Handling

**Problem:** Different endpoints return different error formats
```
// Endpoint 1
{ "error": "Not found" }

// Endpoint 2
{ "code": 404, "message": "Resource not found" }
```

**Solution:** Standardize error format across all endpoints

### Pitfall: God Endpoints

**Problem:** Single endpoint doing too much based on parameters
```
GET /data?type=users&action=delete&id=123
```

**Solution:** Use proper REST structure
```
DELETE /users/123
```

### Pitfall: Ignoring Caching

**Problem:** No cache headers, identical queries repeated
```
GET /users/123
(No Cache-Control or ETag headers)
```

**Solution:** Add cache headers
```
GET /users/123
Cache-Control: public, max-age=300
ETag: "abc123xyz"
```

Clients respect caching, reduce server load.

### Pitfall: Breaking Changes Without Versioning

**Problem:** Removing fields or changing response structure
```
// v1: { "user": { "name": "John" } }
// Now: { "name": "John" }
// Breaks all clients
```

**Solution:**
- Use versioning (URL or header)
- Design for forward compatibility (add fields, don't remove)
- Support deprecated fields for reasonable period

### Pitfall: Poor Pagination

**Problem:** No limits, full result set in every request
```
GET /posts
Returns all 1 million posts (crashes clients)
```

**Solution:** Always paginate
```
GET /posts?limit=20&offset=0
Returns 20 items with pagination metadata
```

### Pitfall: Exposed Internal Details

**Problem:** Error messages revealing system internals
```
ERROR: Unique constraint violation on users_email_idx
```

**Solution:** Generic error codes with details in logs
```
{ "code": "VALIDATION_ERROR", "message": "Email already in use" }
(Log full details server-side)
```

### Pitfall: Inadequate Authentication

**Problem:** No authentication or sending credentials in URL
```
GET /api/data?api_key=secret123
GET /api/data?password=mypassword
```

**Solution:** Use Authorization header with HTTPS
```
GET /api/data
Authorization: Bearer <token>
(HTTPS only)
```

### Pitfall: Missing Request Validation

**Problem:** Accepting any input, failing later in business logic
```
POST /users
{ "name": 123, "email": "not-an-email" }
(No validation, crashes in processing)
```

**Solution:** Validate request schema immediately
```
1. Type check (name: string)
2. Format check (email: valid format)
3. Business rules (email unique, age >= 18)
4. Return 400 if invalid
```

### Pitfall: GraphQL Over/Under Fetching Issues

**Problem (Over-fetching with REST):**
```
GET /users/123
Returns: { id, name, email, phone, address, ... }
Client only needs: id, name
```

**Solution:** Use GraphQL's precise field selection
```graphql
query {
  user(id: "123") {
    id
    name
  }
}
```

**Problem (Under-fetching with GraphQL):**
```graphql
query {
  user(id: "123") { posts { id } }
  user(id: "456") { posts { id } }
  # Separate queries for each user
}
```

**Solution:** Batch queries
```graphql
query {
  user1: user(id: "123") { posts { id } }
  user2: user(id: "456") { posts { id } }
  # Single request, clear
}
```

---

## Quick Reference

**REST Status Codes:**
- `2xx`: Success (200, 201, 204)
- `4xx`: Client error (400, 401, 403, 404, 422, 429)
- `5xx`: Server error (500, 503)

**Authentication:**
- API Key: Simple, good for internal/service APIs
- JWT: Good for public APIs, includes scopes
- OAuth2: Third-party integrations

**Pagination:**
- Offset/limit: Simple, small datasets
- Cursor-based: Large datasets, efficient
- Keyset: Natural sort fields

**GraphQL N+1:**
- Use DataLoader for batching
- Implement in resolver layer
- Transparent to schema

**Error Format:**
```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable message",
  "details": {}
}
```

**Always include:**
- Consistent endpoint structure
- Clear error responses
- Proper status codes
- Pagination on collections
- Authentication/authorization
- Request validation
- Documentation
- Caching headers

---

**Note:** For project-specific API patterns, check `.claude/CLAUDE.md` in the project directory.
