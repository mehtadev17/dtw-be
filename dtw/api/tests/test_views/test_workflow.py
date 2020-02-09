from django.urls import reverse
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.workflow import Workflow
from api.tests.assets.mock_fe_workflow import mock_fe_workflow


class TestWorkflowViewSet(APITestCase):
    fixtures = ["components.json", "schemas.json"]

    @tag('integration')
    def test_create_simple_workflow(self):
        """
        Ensure we can create a new workflow object.
        """
        url = reverse("api:workflow-list")
        data = {
            "name": "Test Workflow", "type": "BATCH",
            "description": "Filter customers who have selected to opt out of emails using customer and optout datasets",
            "version": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), "Test Workflow")
        self.assertEqual("Test Workflow", Workflow.objects.get(id=response.data.get("id")).name)

    @tag('integration')
    def test_create_complicated_workflow(self):
        """
        Ensure we can create a new workflow complicated object.
        """
        url = reverse('api:workflow-list')
        data = mock_fe_workflow
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'POC_Prototype_Workflow')
        self.assertEqual('POC_Prototype_Workflow',
                         Workflow.objects.get(id=response.data.get("id")).name)

    @tag('integration')
    def test_update_complex_workflow(self):
        """
        Ensure we can update a new workflow object with connections and steps.
        """
        create_url = reverse("api:workflow-list")
        data = mock_fe_workflow
        create_response = self.client.post(create_url, data, format="json")
        workflow_data = create_response.json()
        update_url = reverse("api:workflow-detail", args=[str(workflow_data["id"])])
        workflow_data['connections']['graph'] = {'test': 'update'}
        workflow_data['steps'][0]['name'] = 'Test Update'
        workflow_data['steps'][0]['parameters'] = [{'test': 'update'}]
        workflow_data['steps'][0]['schemas'][0]['schema'] = 4
        update_response = self.client.put(update_url, workflow_data, format="json")
        updated_workflow_data = update_response.json()
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Workflow.objects.count())
        self.assertEqual(workflow_data['connections']['graph'], updated_workflow_data['connections']['graph'])
        self.assertEqual(workflow_data['steps'][0]['name'], updated_workflow_data['steps'][0]['name'])
        self.assertEqual(workflow_data['steps'][0]['parameters'], updated_workflow_data['steps'][0]['parameters'])
        self.assertEqual(
            workflow_data['steps'][0]['schemas'][0]['schema'],
            updated_workflow_data['steps'][0]['schemas'][0]['schema']
        )
