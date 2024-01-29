from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    # used to import the signals when the Django application is ready
    def ready(self):
        import products.signals  # noqa -used to tell linters to ignore the warning or error associated with the import statement.