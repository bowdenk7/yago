from django.test import TestCase


class SanityTest(TestCase):
    def test_reality(self):
        self.assertEqual(True, True)