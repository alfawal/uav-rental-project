"""uav_project URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

The logic below is to automatically load all urls.py files from all apps
that start with "uav_project." prefix and add them to urlpatterns under
the specified parent_route prefix.

e.g. uav_project.orders.urls includes:
parent_route = None
urlpatterns of (/all-orders/, /order/<id>/, etc.)
they will be available under /all-orders/, /order/<id>/, etc.

Where as uav_project.users.urls includes:
parent_route = "users/"
urlpatterns of (/login/, logout/, etc.)
they will be available under /users/login/, /users/logout/, etc.
"""

import contextlib
import importlib

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

apps_urls = []
# Iterate over all apps that start with "uav_project." prefix.
for app in (
    my_apps := tuple(
        app
        for app in settings.INSTALLED_APPS
        if app.startswith("uav_project.")
    )
):
    with contextlib.suppress(ImportError):
        # Import urls.py from the app.
        module = importlib.import_module(f"{app}.urls")
        # If the app has urlpatterns: if parent_route is specified, add
        # urlpatterns under the specified parent_route, otherwise add
        # urlpatterns as they are (under "").
        if app_urls := getattr(module, "urlpatterns", None):
            if parent_route := getattr(module, "parent_route", None):
                apps_urls.append(
                    path(
                        parent_route,
                        include(app_urls),
                    ),
                )
            else:
                apps_urls.append(
                    path("", include(app_urls)),
                )


urlpatterns = [
    path("admin/", admin.site.urls),
    *apps_urls,
]

if settings.ENABLE_BROWSABLE_API:
    urlpatterns.append(
        path(
            "api-auth/",
            include("rest_framework.urls", namespace="rest_framework"),
        )
    )

print(f"Loaded apps urls ({len(my_apps)}).")
