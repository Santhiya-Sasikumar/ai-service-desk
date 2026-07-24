import cProfile
import pstats
import io
import requests

def run():
    print("Sending 100 requests to create tickets...")
    for i in range(100):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/tickets/",
                json={
                    "title": f"Login issue {i}",
                    "description": "Created during client-side profiling",
                    "priority": "high",
                    "assignee_email": "user@example.com"
                },
                timeout=5
            )
            # Assert response is successful (200 or 201)
            assert response.status_code in (200, 201), f"Unexpected status code: {response.status_code}"
        except Exception as e:
            print(f"Request failed: {e}")
            break

if __name__ == "__main__":
    # Profile the run() function using cProfile
    cProfile.run("run()")
