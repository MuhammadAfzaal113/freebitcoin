from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from django.conf import settings

from .utils import compare_digest, sha1_hash, md5_hash

from django.contrib.auth import get_user_model

User = get_user_model()


class TestSurveyCallbacks(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        self.user = user

    def test_compare(self):
        assert compare_digest('a', 'a')
        assert compare_digest('a', 'b') is False

    def test_sha1_hash(self):
        msg = 'https://publisher.com/complete?\
uid=8cc877ee-af19-488d-b28d-216fb866b996&val=500'
        hash = sha1_hash(msg, 'JLOIAUNMHFli7ZJOQVEzm98rzqnm9')
        assert hash == 'dbcd6bb8ca677344592842a52b4fca9bec36cd4b'

    def test_md5_hash(self):
        msg = 'a'
        hash = md5_hash(msg)
        assert hash == 'e42235ff5af2c1446a3957f5b380fe06'

    def test_bitlab(self):
        url = str(reverse('landing:bitlab-callback'))
        uid = str(self.user.profile.uid)
        tx = '14056'
        msg = f"https://freeomi.com{url}?uid={uid}&val={100}&tx={tx}"
        data = {
            'uid': uid,
            'val': 100,
            'tx': tx,
            'hash': sha1_hash(msg, settings.BITLAB)
        }
        response = self.client.get(url, data)
        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 100

        response = self.client.get(url, data)
        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 100

    def test_cpx(self):
        url = str(reverse('landing:cpx-callback'))

        user_id = str(self.user.profile.uid)
        trans_id = 'rando'
        status = 1
        amount_local = 200

        msg = f"{user_id}-{settings.CPX_HASH}"
        data = {
            'user_id': user_id,
            'trans_id': trans_id,
            'status': status,
            'amount_local': amount_local,
            'hash': md5_hash(msg)
        }
        response = self.client.get(url, data)
        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 200

        response = self.client.get(url, data)
        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 200

        data['status'] = 2
        response = self.client.get(url, data)
        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 0
