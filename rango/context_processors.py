from rango.models import Category

def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}