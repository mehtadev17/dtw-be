from django.db.models.fields.related import ForeignObjectRel, ManyToManyField


class ItemMergeMixin:
    DEFAULT_PRIMARY_KEY = 'id'

    @staticmethod
    def delete_old_items(old_items):
        if not old_items:
            return
        for key in old_items:
            old_items[key].delete()

    @staticmethod
    def get_instance_fields(instance):
        return {field.name: field for field in instance._meta.get_fields()}

    @staticmethod
    def is_related(field_type):
        return isinstance(field_type, (ForeignObjectRel, ManyToManyField))

    @staticmethod
    def remove_redundant_keys(data_set, redundant_keys):
        if not redundant_keys:
            return

        for key in redundant_keys:
            data_set.pop(key, None)

    @classmethod
    def update_instance(cls, instance, data):
        nested = dict()
        field_types = cls.get_instance_fields(instance)
        for field_name in data:
            if cls.is_related(field_types.get(field_name)):
                nested[field_name] = data[field_name]
            else:
                setattr(instance, field_name, data[field_name])
        return nested

    @staticmethod
    def is_many_to_many(field_type):
        return isinstance(field_type, (ManyToManyField,))

    @classmethod
    def merge_set(cls, objects_set, new_data_set, primary_key=DEFAULT_PRIMARY_KEY, redundant_keys=None):
        """
        Merging two data sets
        :param objects_set: existing objects set
        :param new_data_set: dictionary with new data
        :param primary_key: differences primary key
        :param redundant_keys: redundant keys set, will be not saved
        :param defaults: dictionary with default parameters for create
        :param overrides: dictionary with default parameters for update
        :return: merged object set
        """
        updated_items = []
        related_items = []
        model_class = objects_set.model
        old_items = {
            getattr(item, primary_key): item for item in objects_set.all()
        }

        for item in new_data_set:
            if primary_key in item and item[primary_key] in old_items:
                # Updating existing item
                instance = old_items.pop(item[primary_key])
            else:
                # Creating new item
                item.pop(primary_key, None)
                instance = model_class()

            cls.remove_redundant_keys(item, redundant_keys)
            related_items = cls.update_instance(instance, item)
            if hasattr(objects_set, 'add'):
                objects_set.add(instance, bulk=False)
            instance.save()
            if related_items:
                cls.merge_set_groups(
                    instance,
                    list(related_items.keys()),
                    related_items,
                    redundant_keys=redundant_keys
                )
            updated_items.append(instance)

        cls.delete_old_items(old_items)
        return updated_items

    @classmethod
    def merge_set_groups(cls, instance, relations, validated_data, redundant_keys=None):
        field_types = cls.get_instance_fields(instance)
        for relation in relations:
            field = getattr(instance, relation)
            field_type = field_types.get(relation)
            if cls.is_many_to_many(field_type):
                field.set(validated_data.get(relation), bulk=False)
            else:
                cls.merge_set(
                    field,
                    validated_data.get(relation),
                    redundant_keys=redundant_keys,
                )
