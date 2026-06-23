from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from kanban.bootstrap import bootstrap_admin, bootstrap_default_workspace


class Command(BaseCommand):
    help = "Create or update the default admin account."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--email", required=True)
        parser.add_argument("--password", required=True)

    def handle(self, *args, **options):
        if not options["password"]:
            raise CommandError("Password is required")
        user, created = bootstrap_admin(username=options["username"], email=options["email"], password=options["password"])
        bootstrap_default_workspace(user)
        state = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Admin account {state}: {user.username}"))
