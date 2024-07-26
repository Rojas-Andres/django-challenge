"""
File with the authentication views.
"""

from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import LoginSerializer
from user.models import User


class LoginView(TokenObtainPairView):
    """
    View for handling user authentication requests.

    This view allows users to log in by providing their email and password.
    Upon successful login, it returns a JSON response with the user's details and tokens.

    Inherits from TokenObtainPairView, which generates a JSON Web Token (JWT) for a user.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def handle_exception(self, exc):
        """
        Handle exceptions that occur during the authentication process.

        Overrides the handle_exception method of the parent class to handle AuthenticationFailed exceptions,
        which occur when the user provides incorrect login credentials.

        Args:
            exc: The exception that occurred.

        Returns:
            A JSON response with an error message and status code.

        """
        if isinstance(exc, AuthenticationFailed):
            return Response(
                {"message": "Error login, password incorrect", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().handle_exception(exc)

    def post(self, request):
        """
        Handle POST requests for user authentication.

        Overrides the post method of the parent class to add custom functionality for user authentication.
        It checks if the email and password are provided, checks if the email exists in the database,
        and returns a custom response with the user's details and tokens upon successful login.

        Args:
            request: The HTTP request object.

        Returns:
            A JSON response with the user's details, tokens, and status code.

        """
        request_email = request.data.get("email")
        request_password = request.data.get("password")
        if not request_email or not request_password:
            return Response(
                {"message": "Error Email or Password not found", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("email"):
            user = User.objects.filter(email=request.data["email"]).first()
            if not user:
                return Response(
                    {"message": "Error Email not found", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        response = super().post(request)

        refresh_token = response.data["refresh"]
        access_token = response.data["access"]
        user_id = response.data["id"]
        email = response.data["email"]
        name = response.data["name"]

        return Response(
            {
                "message": "User logged in successfully",
                "user_detail": {
                    "user_id": user_id,
                    "email": email,
                    "name": name,
                },
                "token": {
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                },
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    A view for handling user logout requests.

    This view requires the user to be authenticated and expects a refresh token to be provided in the request data.
    Upon receiving a valid refresh token, the view invalidates it and logs the user out, returning a success message.
    If the token is invalid or an error occurs during the logout process, an appropriate error message is returned.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle the HTTP POST request sent to the LogoutView endpoint.

        This method expects a refresh token to be provided in the request data.
        If the token is valid, it is invalidated and the user is logged out.
        If the token is invalid or an error occurs, an appropriate error message is returned.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success message if the logout is successful,
            or an error message if the token is invalid or an error occurs during the logout process.
        """
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"message": "Error refresh token not found", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            return Response(
                {"message": "Successfully logged out.", "status": status.HTTP_205_RESET_CONTENT},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"message": "Invalid token.", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "Error logout", "error": str(e), "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutAllView(APIView):
    """
    View for logging out all active sessions of a user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate all outstanding tokens for the authenticated user.

        If there are no active tokens for the user, return an error message.
        If the token is invalid, return an error message.
        If there is any other error, return an error message with details.

        Returns:
            A response with a success message if the operation is successful,
            or an error message if there are no active tokens for the user,
            the token is invalid, or there is any other error.
        """
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            if not tokens:
                return Response(
                    {"message": "No active tokens for this user.", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(
                {"message": "Successfully logged out all sessions.", "status": status.HTTP_205_RESET_CONTENT},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"message": "Invalid token.", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "Error logout", "error": e, "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
