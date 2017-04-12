import logging

from .models import UserSession


log = logging.getLogger(__name__)


class UserSessionTrackingMiddleware(object):

    def process_request(self, request):
        request.autometrics_key = (
            request.session.session_key
            if hasattr(request, 'session')
            else None
        )

    def process_response(self, request, response):
        if hasattr(request, 'user'):
            request_key = request.autometrics_key
            if request.session.session_key is None:
                try:
                    request.session.cycle_key()
                except Exception as e:
                    log.critical(
                        'unable to cycle null session key: %s',
                        str(e),
                        )
                    return response
            response_key = request.session.session_key
            if request_key != response_key:
                log.debug(
                    'user {0} session key changed from {1}... to {2}'.format(
                        request.user,
                        request_key[:5] if request_key else '<none>',
                        response_key[:5] if response_key else '<none>',
                    )
                )
                if UserSession.objects.filter(
                        session=request_key
                        ).count() == 0:
                    if UserSession.objects.filter(
                            session=response_key
                            ).count() == 0:
                        response_key = None
                    request_user = (
                        None if request.user.is_anonymous() else request.user
                    )
                    UserSession.objects.create(
                        session=request_key,
                        user=request_user,
                        previous_id=response_key,
                    )
        return response
