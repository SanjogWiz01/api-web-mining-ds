# REST API Design Principles

Good API design is decided once, forever. Follow these principles when you
*design* APIs (used in files 19-30).

## 1. Resources, not actions

Use nouns for URLs, verbs only for HTTP methods.

```
BAD:   /getUser?id=5          /createUser         /deleteUser?id=5
GOOD:  GET    /users/5        POST  /users        DELETE /users/5
```

## 2. Correct HTTP semantics

| Operation   | Method  | Status on success |
|-------------|---------|-------------------|
| Create      | POST    | 201 Created       |
| Read        | GET     | 200 OK            |
| Full update | PUT     | 200 OK            |
| Partial     | PATCH   | 200 OK            |
| Delete      | DELETE  | 204 No Content    |

## 3. Consistent naming

- Plural nouns, lowercase, kebab or underscore separated: `/users`, `/order-items`.
- Nested only one level deep when there is a real parent-child relation:
  `/users/5/orders` — but `GET /orders?user_id=5` is often better.
- Versions in the URL or header: `/v1/users`.

## 4. Status codes say everything

- 2xx success, 4xx client mistakes (with helpful error bodies), 5xx server faults.
- Don't return 200 for everything with an "error" flag in the body.

## 5. Uniform error format

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user with id 5 exists",
    "details": { "id": 5 }
  }
}
```

Keep the shape identical across every endpoint so clients can parse it once.

## 6. Pagination, filtering, sorting, searching

```
GET /users?page=2&limit=50&sort=-created_at&search=sanjo&status=active
```

Return a stable envelope:

```json
{
  "data": [...],
  "meta": { "page": 2, "limit": 50, "total": 1240 },
  "links": { "next": "/users?page=3&limit=50", "prev": "/users?page=1&limit=50" }
}
```

## 7. Idempotency

- GET, PUT, DELETE should be idempotent (repeatable, same result).
- For POST, accept a client-generated `Idempotency-Key` header and store it.

## 8. Versioning

- `/v1/...` in the URL is the most common and simplest.
- Never break old clients: deprecate, warn, then remove.

## 9. Security

- HTTPS everywhere.
- Auth via OAuth2/JWT; never API keys in URLs.
- Validate and rate-limit input; return 401/403 correctly.

## 10. Documentation & contracts

- Auto-generate OpenAPI docs (FastAPI does this for free).
- Document auth, pagination, errors, examples, and rate limits.

## Checklist before you ship

- [ ] Nouns in URLs, methods are verbs
- [ ] Consistent error format
- [ ] Pagination on every list endpoint
- [ ] Versioning strategy decided
- [ ] Auth documented and enforced
- [ ] Rate limiting present
- [ ] Idempotent where promised
- [ ] OpenAPI docs generated
