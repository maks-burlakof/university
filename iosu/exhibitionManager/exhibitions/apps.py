from django.apps import AppConfig


class ExhibitionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exhibitions'
    verbose_name = 'Организация выставки'

    def ready(self):
        from django.core.management import call_command
        from io import StringIO

        with StringIO() as out:
            call_command('makemigrations', 'exhibitions', stdout=out)
            call_command('migrate', stdout=out)
            print('Apply migrations: ', out.getvalue())
