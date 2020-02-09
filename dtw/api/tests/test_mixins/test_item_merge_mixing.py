from django.test import TestCase
from api.models.workflow import Workflow
from api.mixins.item_merge_mixin import ItemMergeMixin


class TestItemMergeMixin(TestCase):

    def test_get_instance_fields(self):
        instance = Workflow(name='test', type='BATCH')
        expected_fields = ['connections', 'steps', 'id', 'name', 'type', 'description',
                           'path', 'created_at', 'updated_at', 'created_by', 'asv', 'bapci', 'lob', 'version']
        actual_fields = list(ItemMergeMixin.get_instance_fields(instance).keys())
        self.assertEqual(expected_fields.sort(), actual_fields.sort())

    def test_is_related(self):
        instance = Workflow(name='test', type='BATCH')
        related_field = instance._meta.get_field('connections')
        self.assertTrue(ItemMergeMixin.is_related(related_field))
        related_field = instance._meta.get_field('name')
        self.assertFalse(ItemMergeMixin.is_related(related_field))

    def test_remove_redundant_keys(self):
        data_set = {'id': 1, 'name': 'test'}
        redundant_keys = ['id']
        ItemMergeMixin.remove_redundant_keys(data_set, redundant_keys)
        self.assertTrue('id' not in data_set)

    def test_update_instance(self):
        instance = Workflow(name='test', type='BATCH')
        data = {'name': 'blah', 'connections': {'graph': {'test': 'test'}}}
        nested_fields = ItemMergeMixin.update_instance(instance, data)
        self.assertEqual('blah', instance.name)
        self.assertIn('connections', nested_fields)
