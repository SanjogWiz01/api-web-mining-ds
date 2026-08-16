"""
📘 TOPIC 25: GraphQL — Query Only What You Need
==============================================
GraphQL lets clients request exactly the fields they want
in a single POST to one endpoint (usually /graphql).

Pros: no over-fetching, no under-fetching, one round trip.
Cons: caching is harder, complexity moves to the server.

Sample query:
  { post(id: 1) { id title body user { name } } }
"""

import requests
import json

GRAPHQL_URL = "https://jsonplaceholder.typicode.com"  # demo (REST echo)


# ─────────────────────────────────────────────
# 1. Build a GraphQL query
# ─────────────────────────────────────────────
def build_query():
    print("\n── GraphQL Query ────────────────────")
    query = """
    query {
      post(id: 1) {
        id
        title
        user {
          name
          email
        }
      }
    }
    """
    print(f"  Query:\n{query}")


# ─────────────────────────────────────────────
# 2. Send a GraphQL-style request
# ─────────────────────────────────────────────
def send_graphql():
    print("\n── Send GraphQL Request ─────────────")
    query = "{ post(id: 1) { id title } }"
    r = requests.post(GRAPHQL_URL + "/posts",
                      json={"query": query, "variables": {}})
    print(f"  Status: {r.status_code}")
    print(f"  Sent body: {json.loads(r.request.body)['query']}")


# ─────────────────────────────────────────────
# 3. GraphQL vs REST comparison
# ─────────────────────────────────────────────
def graphql_vs_rest():
    print("\n── GraphQL vs REST ──────────────────")
    comparison = [
        ("REST", "Many endpoints, one resource each"),
        ("     ", "Over-fetching: whole objects returned"),
        ("GraphQL", "One /graphql endpoint"),
        ("      ", "Client picks exact fields, nested queries"),
    ]
    for label, text in comparison:
        print(f"  {label:<8} {text}")


# ─────────────────────────────────────────────
# 4. Mutations & variables
# ─────────────────────────────────────────────
def mutations_variables():
    print("\n── Mutations & Variables ────────────")
    mutation = """
    mutation CreatePost($input: PostInput!) {
      createPost(input: $input) { id title }
    }
    """
    variables = {"input": {"title": "Hello GraphQL", "body": "via variables"}}
    print(f"  Mutation:\n{mutation}")
    print(f"  Variables: {json.dumps(variables)}")
    print("  Errors come back as {'errors': [...]} in the body, not HTTP codes.")


if __name__ == "__main__":
    print("=" * 55)
    print("  GRAPHQL: query what you need")
    print("=" * 55)
    build_query()
    send_graphql()
    graphql_vs_rest()
    mutations_variables()
    print("\nGraphQL demos complete.")