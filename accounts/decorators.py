from typing import Optional

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def restrict_access(function=None, user_type: Optional[str] = None, redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url='accounts:login'):
    """
    Decorator for views that checks that the logged in user is the selected user_type,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_staff and u.type == user_type,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def decorate_url_patterns(patterns, user_type: str):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = restrict_access(function=callback, user_type=user_type)
        pattern._callback = restrict_access(function=callback, user_type=user_type)
        decorated_patterns.append(pattern)
    return decorated_patterns
