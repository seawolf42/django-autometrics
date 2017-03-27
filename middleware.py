class UserSessionTrackingMiddleware(object):

    def process_request(self, request):
        request.pmetrics_key = request.session.session_key if hasattr(request, 'session') else None

    def process_response(self, request, response):
        print 'RESPONSE ->',
        if hasattr(request, 'user'):
            request_key = request.pmetrics_key
            if request.session.session_key is None:
                request.session.cycle_key()
            response_key = request.session.session_key
            print 'USER:', request.user,
            print 'KEY:', response_key,
            print 'CHANGED:', request_key != response_key
        else:
            print 'STATUS:', response.status_code
        return response
