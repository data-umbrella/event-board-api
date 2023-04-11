from drfpasswordless.utils import CallbackToken


def generate_auth_token(client, user):
    client.post('/auth/email/', {'email': user.email})
    callback_token = CallbackToken.objects.filter(user=user, is_active=True).first()
    challenge_response = client.post('/auth/token/', {
        'email': user.email,
        'token': callback_token,
    })
    return challenge_response.data['token']