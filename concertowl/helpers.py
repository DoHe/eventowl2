def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def as_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj
