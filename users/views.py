from typing import List
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.hashers import check_password
from .schemas import *
from bookhiveConfig.utils import get_api, generate_user_token, refresh_access_token, CustomResponse

User = get_user_model()
api = get_api(
    title="BookHive Users API",
    description="This documentation provides endpoints for managing all users.",
    version="1.0.0"
)


def return_user_data(user):
    # this function returns the details of the passed in user
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        user_type=user.user_type
    ).dict()


@api.post("/signup", response=UserResponseSchema)
@ transaction.atomic
def signup(request, data: UserSignupSchema):
    try:
        # check if a user with that email address already exists
        email = data.email.lower()
        if User.objects.filter(email=email).exists():
            return CustomResponse.failed(message="A user with this email address already exists")

        user = User.objects.create_user(
            email=email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password,
            user_type=data.user_type
        )
        return CustomResponse.success(
            data=return_user_data(user),
            message="Signup successful"
        )
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.post("/login", response=TokenResponseSchema)
def login_user(request, data: UserLoginSchema):
    def validate_user_credentials(data):
        email = data.email.lower()
        password = data.password
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
        else:
            raise ValueError('Invalid email or password')

    # validate user credentials
    try:
        user = validate_user_credentials(data)
    except ValueError as e:
        return CustomResponse.failed(message=str(e))

    # log the user in
    login(request, user)

    # generate tokens for the user
    token = generate_user_token(user)
    return CustomResponse.success(
        data={
            "refresh": token["refresh"],
            "access": token["access"],
            "user_info": return_user_data(user),
        },
        message="Login successful"
    )


@api.get("/users", response=List[UserResponseSchema])
def get_all_users(request, page=1, size=10, id=None, email=None, first_name=None, last_name=None):
    try:
        # only admins and superusers can view all users..
        # a normal user only gets to see his/her own data
        if request.user.user_type == 'user':
            return CustomResponse.success(
                message="User retrieved successfully", 
                data=return_user_data(request.user)
            )

        queryset = User.objects.all().order_by('id')
        # apply filters dynamically based on the id, email, first_name, or last_name
        if id:
            queryset = queryset.filter(id=id)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        # paginate the results
        paginator = Paginator(queryset, size)
        paginated_users = paginator.get_page(page)

        # convert paginated users to a list of dicts
        users = [return_user_data(user) for user in paginated_users.object_list]
        return CustomResponse.success(
            data={
                "users": users,
                "page": page,
                "size": size,
                "total_pages": paginator.num_pages,
                "total_users": paginator.count,
            },
            message="User(s) retrieved successfully"
        )
    except Exception as e: return CustomResponse.failed(message=str(e))


@api.get("/users/{user_id}", response=UserResponseSchema)
def get_user_by_id(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user_info = return_user_data(user)
        return CustomResponse.success(data=return_user_data(user), message="User record retrieved successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.patch("/users/{user_id}", response=UserResponseSchema)
def patch_user(request, user_id, data: UserUpdateSchema):
    try:
        user = get_object_or_404(User, id=user_id)
        for attr, value in data.dict().items():
            if value is not None:
                setattr(user, attr, value)
        user.save()
        user_info = return_user_data(user)
        return CustomResponse.success(data=return_user_data(user), message="User record updated successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.put("/users/{user_id}", response=UserResponseSchema)
def put_user(request, user_id, data: UserUpdateSchema):
    try:
        user = get_object_or_404(User, id=user_id)
        user.email, user.user_type = data.email, data.user_type
        user.first_name, user.last_name = data.first_name, data.last_name
        if data.password:
            user.set_password(data.password)
        user.save()
        user_info = return_user_data(user)
        return CustomResponse.success(data=return_user_data(user), message="User record updated successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.delete("/users/{user_id}", response=dict)
def delete_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return CustomResponse.success(message="User deleted successfully", status=204)
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.post("/token/refresh", response=dict)
def refresh_token(request, data: TokenRefreshSchema):
    # generates a new access token using the provided refresh token
    try:
        # call the function to generate a new access token
        result = refresh_access_token(data.refresh_token)
        return result
    except Exception as e:
        return CustomResponse.failed(message=str(e))

