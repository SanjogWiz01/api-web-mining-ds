from fastapi import FastAPI, HTTPException, Query
from typing import Optional, Any, List
from pydantic import BaseModel

app = FastAPI(title="Recursive Functions", description="Demonstrating recursion with FastAPI")


# ████████████████████████████████████████████████████████████████████████████████
# RECURSIVE FUNCTION 1: Factorial
# ████████████████████████████████████████████████████████████████████████████████

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# ████████████████████████████████████████████████████████████████████████████████
# RECURSIVE FUNCTION 2: Fibonacci
# ████████████████████████████████████████████████████████████████████████████████

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ████████████████████████████████████████████████████████████████████████████████
# RECURSIVE FUNCTION 3: Flatten nested lists
# ████████████████████████████████████████████████████████████████████████████████

def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# ████████████████████████████████████████████████████████████████████████████████
# RECURSIVE FUNCTION 4: Nested comment tree traversal
# ████████████████████████████████████████████████████████████████████████████████

class Comment(BaseModel):
    id: int
    text: str
    replies: List["Comment"] = []

Comment.model_rebuild()


nested_comments_db = Comment(
    id=1,
    text="What a great post!",
    replies=[
        Comment(id=2, text="Totally agree!", replies=[
            Comment(id=3, text="Me too!", replies=[]),
        ]),
        Comment(id=4, text="I have a different opinion.", replies=[
            Comment(id=5, text="Why is that?", replies=[
                Comment(id=6, text="Because...", replies=[]),
            ]),
        ]),
    ],
)


def count_all_comments(comment: Comment) -> int:
    count = 1
    for reply in comment.replies:
        count += count_all_comments(reply)
    return count


def collect_all_text(comment: Comment, depth: int = 0) -> list[dict]:
    entries = [{"id": comment.id, "text": comment.text, "depth": depth}]
    for reply in comment.replies:
        entries.extend(collect_all_text(reply, depth + 1))
    return entries


# ████████████████████████████████████████████████████████████████████████████████
# RECURSIVE FUNCTION 5: GCD (Euclidean algorithm)
# ████████████████████████████████████████████████████████████████████████████████

def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


# ████████████████████████████████████████████████████████████████████████████████
# FASTAPI ENDPOINTS
# ████████████████████████████████████████████████████████████████████████████████

@app.get("/")
def root():
    return {
        "message": "Recursive Functions Demo",
        "endpoints": {
            "factorial": "/factorial/{n}",
            "fibonacci": "/fibonacci/{n}",
            "flatten": "/flatten",
            "comments/tree": "/comments/tree",
            "comments/count": "/comments/count",
            "gcd": "/gcd/{a}/{b}",
        },
    }


@app.get("/factorial/{n}")
def get_factorial(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    if n > 100:
        raise HTTPException(status_code=400, detail="n too large (max 100)")
    return {"n": n, "factorial": factorial(n)}


@app.get("/fibonacci/{n}")
def get_fibonacci(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    if n > 35:
        raise HTTPException(status_code=400, detail="n too large (max 35 for performance)")
    return {"n": n, "fibonacci": fibonacci(n)}


@app.post("/flatten")
def flatten_nested(data: list):
    return {
        "original": data,
        "flattened": flatten(data),
    }


@app.get("/comments/tree")
def get_comment_tree():
    return collect_all_text(nested_comments_db)


@app.get("/comments/count")
def get_comment_count():
    return {"total_comments": count_all_comments(nested_comments_db)}


@app.get("/gcd/{a}/{b}")
def get_gcd(a: int, b: int):
    if a == 0 and b == 0:
        raise HTTPException(status_code=400, detail="gcd(0, 0) is undefined")
    return {"a": a, "b": b, "gcd": gcd(abs(a), abs(b))}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
