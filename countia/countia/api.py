from ninja import Schema
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


class UserSchema(Schema):
    email: str
    password: str


api = NinjaExtraAPI(
    auth=GlobalAuth(),
    csrf=False
)
api.register_controllers(NinjaJWTDefaultController)


@api.post("/user", auth=None)
def sign_up(request, data: UserSchema):
    userQuery = User.objects.filter(email=data.email)

    if userQuery.exists():
        return {"error": "User already exists"}

    user = User.objects.create(
        email=data.email,
        password=make_password(data.password),
    )
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
