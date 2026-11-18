from django.http import JsonResponse

HEALTH_CHECK_PATHS = ("/health", "/health/")


class AWSHealthCheckMiddleware:
    """Short-circuits AWS Load Balancer health checks before host/CSRF checks."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET" and request.path in HEALTH_CHECK_PATHS:
            return JsonResponse({"status": "ok"}, status=200)
        return self.get_response(request)