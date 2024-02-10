# middleware.py
import timeit

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = timeit.default_timer()
        response = self.get_response(request)
        end_time = timeit.default_timer()

        processing_time = end_time - start_time
        print(f"Page took {processing_time:.6f} seconds to load.")

        return response
