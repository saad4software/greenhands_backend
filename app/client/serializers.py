from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import *
from app.msgs import *
from django.core.mail import send_mail


class AnonymousLoginSerializer(serializers.Serializer):
    print = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    def validate_print(self, data):
        if len(data) < 6:
            raise serializers.ValidationError(error_invalid_print)
        return data

    def validate_role(self, data):
        if data not in ['G', 'T']:
            raise serializers.ValidationError(error_invalid_role)
        return data

    def validate(self, attrs):
        user = self.get_user(attrs)
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': str(user.role)
        }
        return data

    def get_user(self, validate_data):
        user = get_user_model().objects.filter(username=validate_data['print']).first()
        if not user:
            user = get_user_model().objects.create_user(username=validate_data['print'], role=validate_data['role'])
            user.set_password('12345678')
            user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    print = serializers.CharField(source='username', required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    lat = serializers.FloatField(required=True)
    lng = serializers.FloatField(required=True)

    def validate_role(self, data):
        if data not in ["O"]:
            raise serializers.ValidationError(error_invalid_role)
        return data

    def validate_email(self, data):
        user = get_user_model().objects.filter(email=data).first()
        if user:
            raise serializers.ValidationError(error_already_exists)
        return data

    def validate_print(self, data):
        user = get_user_model().objects.filter(username=data).first()
        if user:
            raise serializers.ValidationError(error_already_exists)
        return data

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        # email verification code, assumed username is email!
        code = Code(user=user)
        code.save()

        # send_mail(
        #     'Activation Code',
        #     'Your activation code is ' + str(code.code),
        #     'comeover@detailsb2b.com',
        #     [validated_data['username']],
        #     fail_silently=False,
        #     )

        return user

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'role', 'address', 'password', 'print',
            'first_name', 'last_name', 'phone', 'lat', 'lng',
        )
        read_only_fields = ('id',)


class UserDataCheckSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    lat = serializers.FloatField(required=True)
    lng = serializers.FloatField(required=True)

    def validate_role(self, data):
        if data not in ["O", "T", "G"]:
            raise serializers.ValidationError(error_invalid_role)
        return data

    def validate_print(self, data):
        user = get_user_model().objects.filter(username=data).first()
        if user:
            raise serializers.ValidationError(error_already_exists)
        return data

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'role', 'address', 'password', 'username',
            'first_name', 'last_name', 'phone', 'lat', 'lng',
        )
        read_only_fields = ('id',)


class UserUpdateSerializer(serializers.ModelSerializer):

    def validate_email(self, data):
        user = get_user_model().objects.filter(email=data).first()
        if self.instance.email and user != self.instance:
            raise serializers.ValidationError(error_already_exists)
        return data

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email', 'address', 'phone', 'lat', 'lng', 'role',
        )
        read_only_fields = ('role',)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context.user

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError("Wrong password")
        self.change_password(user, validate_data=data)
        return data

    def change_password(self, user, validate_data):
        user.set_password(validate_data.get('new_password'))
        user.save()


class ProvideNeedSerializer(serializers.Serializer):
    need_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=False, default='')

    def validate_need_id(self, value):
        need = self.get_instance(value)
        if not need:
            raise serializers.ValidationError('doesnt_exist')
        if need.giver:
            raise serializers.ValidationError('already_satisfied')
        return value

    def get_instance(self, value):
        return Need.objects.filter(pk=value).first()


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='datafile', read_only=True)

    class Meta:
        model = Photo
        fields = ['created', 'datafile', 'width', 'height', 'name', 'id']
        read_only_fields = ('created', 'datafile', 'width', 'height', 'name', 'id')


class CategorySerializer(serializers.ModelSerializer):
    icon_model = PhotoSerializer(source='icon', read_only=True)
    icon = serializers.IntegerField(write_only=True)

    class Meta:
        model = Category
        fields = ['name', 'id', 'icon', 'icon_model']
        ordering = ['name']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['title', 'brief', 'created']
        ordering = ['created']


class NeedSerializer(serializers.ModelSerializer):
    category_model = CategorySerializer(source='category', read_only=True)
    granted = serializers.SerializerMethodField()

    def get_granted(self, model):
        return True if model.giver else False

    class Meta:
        model = Need
        fields = ['name', 'id', 'images', 'brief', 'category', 'category_model', 'point', 'granted']
        ordering = ['name']
        extra_kwargs = {'category': {'write_only': True}}


class PointSerializer(serializers.ModelSerializer):
    needs_list = serializers.SerializerMethodField()

    def get_needs_list(self, model):
        qs = Need.objects.filter(point=model, active=True, giver=None)
        serializer = NeedSerializer(qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Point
        fields = [
            'name',
            'images',
            'lat',
            'lng',
            'brief',
            'id',
            'address',
            'needs_list',
        ]
        ordering = ['name', ]


class VerificationRequestSerializer(serializers.ModelSerializer):
    organizer_id = serializers.IntegerField(required=True, write_only=True)
    message = serializers.CharField(required=False, default='')
    sender_model = UserSerializer(source='sender', read_only=True)

    def validate_organizer_id(self, value):
        organizer = self.get_organizer(value)
        if not organizer:
            raise serializers.ValidationError('doesnt_exist')

        return value

    def get_organizer(self, value):
        return User.objects.filter(pk=value, role="O", is_active=True).first()

    class Meta:
        model = VerificationRequest
        fields = [
            'id',
            'status',
            'created',
            'organizer_id',
            'sender_model',
            'message',
        ]
        ordering = ['name', ]
        read_only_fields = ('status', 'created', 'code')


class ConfirmRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(required=True)
    status = serializers.CharField(max_length=1, required=True)
    message = serializers.CharField(required=False, default='')

    def validate_request_id(self, value):
        request = VerificationRequest.objects.filter(pk=value, active=True)
        if not request:
            raise serializers.ValidationError('invalid_request')

        return value

    def validate_status(self, value):
        if value not in ["V", "R"]:
            raise serializers.ValidationError('invalid_status')
        return value

    def save(self, **kwargs):
        if self.data.get('status') == 'V':
            self.verify_account()
        elif self.data.get('status') == 'R':
            self.reject_account()

    def verify_account(self):
        request = VerificationRequest.objects.get(pk=self.data.get('request_id'))

        sender = request.sender
        sender.verified_by = self.context.user
        sender.save()

        request.status = 'V'
        request.save()

        notification = Notification(
            user=sender,
            sender=self.context.user,
            title="Verify",
            brief=self.data.get('message')
        )
        notification.save()

    def reject_account(self):
        request = VerificationRequest.objects.get(pk=self.data.get('request_id'))
        sender = request.sender
        request.status = 'R'
        request.save()

        notification = Notification(
            user=sender,
            sender=self.context.user,
            title="Reject",
            brief=self.data.get('message')
        )
        notification.save()
