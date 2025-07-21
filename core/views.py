from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import escape

class JobApplicationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            form_data = request.data
            cv = request.FILES.get('cv')
            sia_license = request.FILES.get('siaLicense')
            photo_id = request.FILES.get('photoId')
            proof_address = request.FILES.get('proofOfAddress')

            # 🔽 Add your logo URL here
            logo_url = "https://indiguard-backend.onrender.com/static/images/indiguard_logo.jpeg"

            # 🔽 Start the email body with the logo
            html_body = f"""
                <div style="text-align:center;">
                    <img src="{logo_url}" alt="Indiguard Logo" style="width: 100px; height: auto;" />
                </div>
            """

            # 🔽 Add form content
            for key, value in form_data.items():
                label = key.replace('_', ' ').capitalize()
                html_body += f"<p><b>{escape(label)}:</b> {escape(str(value))}</p>"

            subject = f"New Job Application from {form_data.get('fullName')}"
            email = EmailMessage(subject, html_body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
            email.content_subtype = "html"  # Make the email HTML

            # 🔽 Attach uploaded files
            for file, label in [
                (cv, "CV"),
                (sia_license, "SIA License"),
                (photo_id, "Photo ID"),
                (proof_address, "Proof of Address"),
            ]:
                if file:
                    email.attach(f"{label}-{file.name}", file.read(), file.content_type)

            email.send()

            return Response({"message": "Application received successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import json # Import json for clearer parsing if needed, though request.data usually handles it

class QuoteRequestView(APIView):
    def post(self, request):
        # request.data handles JSON parsing for DRF
        # It correctly parses application/json bodies into Python dictionaries
        data = request.data

        # Define the fields that must be present and non-empty (excluding consent for now)
        standard_required_fields = ['name', 'email', 'phone', 'serviceInterest', 'location']

        # --- VALIDATION ---
        errors = {}

        # 1. Check for standard missing/empty fields
        for field in standard_required_fields:
            # Check if field is not in data, or if it's an empty string after stripping whitespace
            if field not in data or not str(data.get(field, '')).strip(): # Ensure value is not just whitespace
                errors[field] = f'{field.capitalize()} is required.'

        # 2. Specific validation for email format (optional, but good practice)
        email = data.get('email')
        if email and not '@' in email: # Basic check, a regex is better
             errors['email'] = 'Invalid email format.'

        # 3. Specific validation for consent (must be True)
        # Check if 'consent' key exists AND its value is explicitly True
        if 'consent' not in data or not data.get('consent') is True:
            errors['consent'] = 'Consent is required to submit the form.'


        # If any errors were found, return 400 Bad Request
        if errors:
            return Response({'error': 'Validation Failed', 'details': errors}, status=status.HTTP_400_BAD_REQUEST)

        # 📩 Email content (your existing logic, slightly adjusted for data access after validation)
        subject = "New Security Quote Request"
        text_content = f"""
New quote request submitted:

Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone')}
Service Interest: {data.get('serviceInterest')}
Location: {data.get('location')}
Service Date: {data.get('serviceDate') or 'N/A'}
Service Duration: {data.get('serviceDuration') or 'N/A'}
Message: {data.get('message') or 'None'}
Consent Given: {"Yes" if data.get('consent') else "No"}
"""

        html_content = f"""
        <html>
        <head>
          <style>
            .container {{
              font-family: Arial, sans-serif;
              background-color: #f9f9f9;
              padding: 20px;
              border-radius: 6px;
              border: 1px solid #e0e0e0;
              max-width: 600px;
              margin: auto;
            }}
            .logo {{
              text-align: center;
              margin-bottom: 20px;
            }}
            .logo img {{
              max-height: 60px;
            }}
            .company-name {{
              text-align: center;
              font-size: 24px;
              font-weight: bold;
              color: #1f2937;
              margin-bottom: 30px;
            }}
            .label {{
              font-weight: bold;
              color: #333;
              margin-top: 10px;
            }}
            .value {{
              color: #555;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="logo">
              <img src="https://indiguard-backend.onrender.com/static/images/indiguard_logo.jpeg" alt="Company Logo" />
            </div>
            <div class="company-name">IndiGuard Security</div>

            <div class="label">Name:</div><div class="value">{data.get('name')}</div>
            <div class="label">Email:</div><div class="value">{data.get('email')}</div>
            <div class="label">Phone:</div><div class="value">{data.get('phone')}</div>
            <div class="label">Service Interest:</div><div class="value">{data.get('serviceInterest')}</div>
            <div class="label">Location:</div><div class="value">{data.get('location')}</div>
            <div class="label">Service Date:</div><div class="value">{data.get('serviceDate') or 'N/A'}</div>
            <div class="label">Service Duration:</div><div class="value">{data.get('serviceDuration') or 'N/A'}</div>
            <div class="label">Message:</div><div class="value">{data.get('message') or 'None'}</div>
            <div class="label">Consent:</div><div class="value">{"Yes" if data.get('consent') else "No"}</div>
          </div>
        </body>
        </html>
        """

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({'success': 'Quote request sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the full exception for debugging on the server side
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Error sending quote request email:")
            return Response({'error': 'Internal server error during email sending. ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# core/views.py
# core/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Testimonial
from .serializers import TestimonialSerializer, AdminTestimonialSerializer
# Make sure to import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny # <--- Add AllowAny here

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()

    def get_serializer_class(self):
        # Use AdminTestimonialSerializer for admin actions, otherwise TestimonialSerializer
        if self.request.user.is_staff:
            return AdminTestimonialSerializer
        return TestimonialSerializer

    def get_permissions(self):
        """
        Set different permissions for different actions.
        - GET (list): Anyone can read approved testimonials.
        - POST (create): Anyone can create a testimonial (it will be unapproved by default).
        - PUT/PATCH/DELETE: Only admin users can modify/delete testimonials.
        """
        # TEMPORARY: For debugging CORS/permission issues during submission.
        # This allows ALL requests to ALL actions on this ViewSet.
        # REMEMBER TO REVERT THIS AFTER DEBUGGING!
        permission_classes = [AllowAny] # <--- Add this line here
        return [permission() for permission in permission_classes] # <--- Keep this line as is

        # ORIGINAL PERMISSIONS (Uncomment and replace the above two lines after debugging):
        # if self.action in ['list', 'create']:
        #     permission_classes = [IsAuthenticatedOrReadOnly]
        # elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
        #     permission_classes = [IsAdminUser]
        # else:
        #     permission_classes = [IsAdminUser]
        # return [permission() for permission in permission_classes]


    def get_queryset(self):
        """
        Allow fetching all testimonials for admin, but only approved for public.
        """
        if self.action == 'list' and not self.request.user.is_staff:
            return Testimonial.objects.filter(approved=True)
        return Testimonial.objects.all()

    # Custom action to approve a testimonial (callable by admin)
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        testimonial = self.get_object()
        testimonial.approved = True
        testimonial.save()
        serializer = self.get_serializer(testimonial)
        return Response(serializer.data)

    # Custom action to reject a testimonial (callable by admin)
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        testimonial = self.get_object()
        testimonial.approved = False # Or delete it, depending on your workflow
        testimonial.save()
        serializer = self.get_serializer(testimonial)
        return Response(serializer.data)
