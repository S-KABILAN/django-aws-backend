# backend/api/middleware.py
class DisableThrottlingMiddleware:
    """
    Middleware to completely disable throttling for development
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Remove any throttling-related headers
        if hasattr(request, 'throttle'):
            request.throttle = None
        
        response = self.get_response(request)
        
        # Remove throttling headers from response
        if hasattr(response, 'headers'):
            response.headers.pop('X-Throttle-State', None)
            response.headers.pop('Retry-After', None)
        
        return response
