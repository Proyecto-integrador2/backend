from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default roles for the application'

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        waiter_group, created = Group.objects.get_or_create(name='Mesero')

        # Asignar permisos a los grupos
        admin_permissions = Permission.objects.all()  # Dar todos los permisos a los administradores
        waiter_permissions = Permission.objects.filter(codename__in=['view_pedido', 'add_pedido'])  # Ejemplo de permisos
        
        admin_group.permissions.set(admin_permissions)
        waiter_group.permissions.set(waiter_permissions)

        self.stdout.write(self.style.SUCCESS('Roles creados satisfactoriamente'))
