from django.urls import reverse
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase
from api.models.function import Function

class TestFunctionViewSet(APITestCase):
    fixtures = ["functions.json"]

    @tag('integration')
    def test_create_simple_function(self):
        """
        Ensure we can create a new function object.
        """
        url = reverse("api:function-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("toInteger", Function.objects.get(id=1).name)
        print("finished")
