from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Access for superusers only."""
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('about:index')


class SuperuserOrAuthorMixin(UserPassesTestMixin):
    """Access for superusers or authors."""
    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user.username == self.kwargs.get("username"))

    def handle_no_permission(self):
        return redirect('about:index')
