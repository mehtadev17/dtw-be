import json

with open('./api/tests/assets/test_workflow.json', 'r') as workflow_json:
    workflow = json.loads(workflow_json.read())

mock_fe_workflow = workflow
