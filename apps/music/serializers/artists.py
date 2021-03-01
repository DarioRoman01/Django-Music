"""Artist serializers."""

# Rest framework
from rest_framework import serializers

# Jwt
import jwt

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# Models
from apps.music.models import Artist
from apps.users.models import User

# Utils
from _datetime import timedelta

class ArtistModelSerializer(serializers.ModelSerializer):
    """Artist model serializer."""

    class Meta:
        """Meta class."""
        model = Artist
        fields = ('artist_name', 'picture')


class CreateArtistSerializer(serializers.Serializer):
    """Create artist serializer."""

    artist_name =  serializers.CharField(max_length=60)
    picture = serializers.ImageField(required=False)

    def create(self, data):
        """Handle artist profile creation."""
        
        user = self.context['user']
        artist = Artist.objects.create(user=user, **data)
        self.send_confirmation_email(user)
        return artist


    def send_confirmation_email(self, user):
        """Send a verification token to become an artist."""
        verificatoin_token = self.gen_verication_token(user)
        subject = 'Congratulations {} your one step close to become and artist'.format(user.username)
        from_email = 'Contact List <noreply@contactlist.com>'
        text_content = render_to_string(
            'artist_verification.html',
            {'token': verificatoin_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(text_content, "text/html")
        msg.send()


    def gen_verication_token(self, user):
        """Gen a verification token to let the user
        have artist status in the app."""

        exp_date = timezone.now() + timedelta(days=2)
        playload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'artist_verification'
        }
        token = jwt.encode(playload, settings.SECRET_KEY, algorithm='HS256')

        return token

class ArtistVerificationSerializer(serializers.Serializer):
    """Artist verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            playload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired. :(')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token:(')

        finally:
            if playload['type'] != 'artist_verification':
                raise serializers.ValidationError('Invalid token type')
            self.context['payload'] = playload
            return data

    def save(self):
        """Update users status to artist."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_artist = True
        user.save()
        return user.artist