from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from django.contrib.auth import get_user_model

User = get_user_model()


class TestView(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        self.user = user

    def set_up_survey_token(self):
        baker.make(
            'panel.SurveyToken', user=self.user, amount=100,
            _quantity=3)

    def set_up_survey_token2(self):
        baker.make(
            'panel.SurveyToken', user=self.user, amount=1000000,
            _quantity=3)

    def set_up_redeemed_token(self):
        baker.make(
            'panel.RedeemedToken', user=self.user, amount=100,
            _quantity=3)

    def test_get_token_balance(self):
        assert float(self.user.get_token_balance()) == 0
        self.set_up_survey_token()
        assert float(self.user.get_token_balance()) == 300

        self.set_up_redeemed_token()
        assert float(self.user.get_token_balance()) == 0

    def test_redeem(self):
        url = str(reverse('panel:redeem'))

        self.set_up_survey_token2()
        self.client.force_login(self.user)
        response = self.client.post(
            url, {'amount': 10000}, HTTP_ACCEPT='application/json')

        assert response.status_code == 200
        assert float(self.user.get_token_balance()) == 2990000

    def test_redeem_min_token(self):
        url = str(reverse('panel:redeem'))

        self.client.force_login(self.user)
        response = self.client.post(
            url, {'amount': 50}, HTTP_ACCEPT='application/json')
        assert response.status_code == 400
        self.assertEqual(response.json()['message'], 'Minimum amount is 100')

    def test_redeem_invalid_amount(self):
        url = str(reverse('panel:redeem'))

        self.client.force_login(self.user)
        response = self.client.post(
            url, {'amount': 100}, HTTP_ACCEPT='application/json')
        assert response.status_code == 400
        self.assertEqual(
            response.json()['message'], 'You do not have enough tokens')

    def test_earn_more(self):
        url = str(reverse('panel:earn_more'))

        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_earn_more_post(self):
        url = str(reverse('panel:earn_more'))

        tabs = ['bitlab', 'cpx']

        self.client.force_login(self.user)

        for tab in tabs:
            response = self.client.post(
                url, {'tab': tab}, HTTP_ACCEPT='application/json')
            assert response.status_code == 200
            assert response.json()['content']
