from django.core.management.base import BaseCommand
from hub.models import Item, CartItem, Message, OrderItem, Order


class Command(BaseCommand):
    help = 'Remove all items and related data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        # Count items before deletion
        item_count = Item.objects.count()
        cart_item_count = CartItem.objects.count()
        message_count = Message.objects.count()
        order_item_count = OrderItem.objects.count()
        order_count = Order.objects.count()

        if item_count == 0:
            self.stdout.write(
                self.style.WARNING('No items found in the database.')
            )
            return

        # Show what will be deleted
        self.stdout.write(
            self.style.WARNING(
                f'This will delete:\n'
                f'- {item_count} items\n'
                f'- {cart_item_count} cart items\n'
                f'- {message_count} messages\n'
                f'- {order_item_count} order items\n'
                f'- {order_count} orders\n'
            )
        )

        # Confirm unless --force is used
        if not options['force']:
            confirm = input('Are you sure you want to proceed? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(
                    self.style.ERROR('Operation cancelled.')
                )
                return

        try:
            # Delete all related data
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Message.objects.all().delete()
            CartItem.objects.all().delete()
            Item.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully removed all {item_count} items and related data.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error removing items: {str(e)}')
            ) 