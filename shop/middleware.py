"""
Rate limiting middleware for NFT downloads
Prevents abuse by limiting download attempts per user
"""
import time

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


class DownloadRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to download URLs
        if '/shop/download/' in request.path and request.user.is_authenticated:
            cache_key = f"download_limit_{request.user.id}"
            attempts = cache.get(cache_key, 0)
            
            # Allow 10 downloads per hour per user
            if attempts >= 10:
                return HttpResponse(
                    "Download limit exceeded. Please try again later.", 
                    status=429
                )
            
            # Increment counter
            cache.set(cache_key, attempts + 1, 3600)  # 1 hour timeout
        
        response = self.get_response(request)
        return response