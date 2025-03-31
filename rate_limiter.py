from collections import deque
import time

class RateLimiter:
    def __init__(self, limit=5, window=1):
        self.limit = limit  # Max requests per second
        self.window = window  # Time window (1 second)
        self.user_requests = {}  # Dictionary to track user requests
    
    def is_allowed(self, user_id):
        current_time = time.time()  # Get current timestamp
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()  # Create queue for user
        
        request_queue = self.user_requests[user_id]
        
        # Remove timestamps older than the time window (1 second)
        while request_queue and request_queue[0] < current_time - self.window:
            request_queue.popleft()
        
        if len(request_queue) < self.limit:
            request_queue.append(current_time)  # Log the new request
            return True  # Allow request
        else:
            return False  # Reject request (rate limit exceeded)

# Testing the Rate Limiter
limiter = RateLimiter()

user_id = "user_123"
for i in range(10):  # Simulate 10 requests
    if limiter.is_allowed(user_id):
        print(f"Request {i+1} allowed ✅")
    else:
        print(f"Request {i+1} blocked ❌")
    time.sleep(0.2)  # Simulating request interval
