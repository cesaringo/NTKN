from django.core.exceptions import ValidationError

def validate_id_exists(model):
    def validate(value):
        if value:
            item = model.objects.filter(id=value)
            if not item:
                raise ValidationError('item with id={0} does not exist.'.format(value))
    return validate

