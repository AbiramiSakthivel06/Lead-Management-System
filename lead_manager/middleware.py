class NoCacheMiddleware:
    """
    Middleware that prevents browser caching of sensitive pages for authenticated users.
    Ensures that clicking the browser back button after logging out forces a refresh
    and redirects the user to the login page instead of displaying cached user data.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Apply no-cache headers strictly to authenticated users' views
        if hasattr(request, 'user') and request.user.is_authenticated:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = 'Sat, 01 Jan 2000 00:00:00 GMT'
            
        return response
