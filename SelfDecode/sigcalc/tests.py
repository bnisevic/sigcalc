from django.test import TestCase, override_settings
from .views import SigcalcView


class SigcalcTestCase(TestCase):

    def test__get_notconverted(self):
        view = SigcalcView()
        post = {'visitorsA': 5, 'visitorsB': 3, 'convertedA': 1, 'convertedB': 3}
        result = view._get_notconverted(post)

        self.assertEqual(result['A'], 4)
        self.assertEqual(result['B'], 0)

    def test_post(self):
        response = self.client.post(
            '',
            data={'visitorsA': '24', 'visitorsB': '5', 'convertedA': '6', 'convertedB': 1},
            ** {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"significance": "No", "pvalue": 0.74}')
