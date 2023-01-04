from urllib.parse import urlparse

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, resolve_url


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Access for superusers only."""
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("about:index")


class SuperuserOrAuthorMixin(UserPassesTestMixin):
    """Access for superusers or authors.
       If user is not authenticated, redirects to login page."""
    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user.username == self.kwargs.get("username"))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (
                (not login_scheme or login_scheme == current_scheme)
                and (not login_netloc or login_netloc == current_netloc)
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        return redirect("about:index")
