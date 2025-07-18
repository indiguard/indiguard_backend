# from django.urls import path
# from .views import JobApplicationView
# from .views import QuoteRequestView


# urlpatterns = [
#     path('apply/', JobApplicationView.as_view(), name='apply'),
#        path('quote-request/', QuoteRequestView.as_view(), name='quote-request'),
# ]



# # core/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TestimonialViewSet

# router = DefaultRouter()
# router.register(r'testimonials', TestimonialViewSet) # The API endpoint will still be /api/testimonials/

# urlpatterns = [
#     path('', include(router.urls)),
# ]



# core/urls.py
# Make sure to import ALL the views that this urls.py will route to
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet, QuoteRequestView, JobApplicationView # <-- IMPORTANT: Add QuoteRequestView and JobApplicationView

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet) # This will create paths like /api/testimonials/

urlpatterns = [
    # Include the router URLs. The '' means it's relative to the /api/ prefix.
    path('', include(router.urls)),

    # Add your specific API paths for quote requests and job applications
    # These paths will also be relative to the 'api/' prefix from your main urls.py
    # So, they will be accessible at /api/quote-request/ and /api/apply/
    path('quote-request/', QuoteRequestView.as_view(), name='quote-request'),
    path('apply/', JobApplicationView.as_view(), name='apply'),
]
