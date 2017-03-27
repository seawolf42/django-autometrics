class UserSessionTrackingMiddleware(object):

    def process_request(self, request):
        print 'REQUEST ->',
        request.pmetrics_key = request.session.session_key if hasattr(request, 'session') else None
        print 'KEY:', request.pmetrics_key

    def process_response(self, request, response):
        print 'RESPONSE ->',
        try:
            request_key = request.pmetrics_key
        except AttributeError:
            request_key = None
        try:
            if request.session.session_key is None:
                request.session.cycle_key()
            response_key = request.session.session_key
        except AttributeError:
            response_key = None
        print 'KEY:', response_key,
        print 'CHANGED:', request_key != response_key,
        print 'USER:', request.user if hasattr(request, 'user') else None
        return response
