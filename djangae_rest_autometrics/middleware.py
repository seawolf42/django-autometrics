import logging


log = logging.getLogger(__name__)


class UserSessionTrackingMiddleware(object):

    def process_request(self, request):
        request.pmetrics_key = (
            request.session.session_key
            if hasattr(request, 'session')
            else None
        )

    def process_response(self, request, response):
        if hasattr(request, 'user'):
            request_key = request.pmetrics_key
            if request.session.session_key is None:
                request.session.cycle_key()
            response_key = request.session.session_key
            if request_key != response_key:
                log.info(
                    'user {0} session key changed from {1}... to {2}'.format(
                        request.user,
                        request_key[:5] if request_key else '<none>',
                        response_key[:5],
                    )
                )
        return response
