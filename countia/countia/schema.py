from typing import Type, Dict
from ninja_jwt.schema import TokenObtainInputSchemaBase
from ninja import Schema
from ninja_jwt.tokens import RefreshToken


class UserSchema(Schema):
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class TokenObtainPairSchema(TokenObtainInputSchemaBase):

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return MyTokenObtainPairOutSchema

    @classmethod
    def get_token(cls, user) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        # this will be needed when creating output schema
        values.update(user=UserSchema.from_orm(user))
        return values
