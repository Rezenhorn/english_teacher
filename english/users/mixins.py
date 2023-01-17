from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class SuperuserOrAuthorMixin(UserPassesTestMixin):
    """Access for superusers or authors."""
    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user.pk == self.kwargs.get("user_id"))

    def handle_no_permission(self):
        return redirect("about:index")
