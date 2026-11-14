
from swagger_coverage_tool import SwaggerCoverageTracker
import httpx

tracker = SwaggerCoverageTracker(service="api-course")

@tracker.track_coverage_httpx("/api/v1/users/{user_id}")
def get_user(user_id: str) -> httpx.Response:
    return httpx.get(f"http://localhost:8000api/v1/users{user_id}")

@tracker.track_coverage_httpx("/api/v1/users")
def post_user() -> httpx.Response:
    return httpx.post("http://localhost:8000api/v1/users")



