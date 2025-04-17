from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication that doesn't enforce CSRF validation.
    """
    def enforce_csrf(self, request):
        # Do not enforce CSRF
        return 