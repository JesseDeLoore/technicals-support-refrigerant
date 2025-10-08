from django.core.management.base import BaseCommand
from ...models import Vessel
import threading


class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def add_arguments(self, parser):
        parser.add_argument("withdraw_amount", nargs="?", type=int, default=10)

    def handle(self, *args, **kwargs):
        vessel = Vessel.objects.create(name="Test Vessel", content=50.0)
        self.stdout.write("Simulating condition...")
        self.run_simulation(vessel.id, kwargs["withdraw_amount"])

    def run_simulation(self, vessel_id:int, amount:int):
        barrier = threading.Barrier(2)

        def user1():
            barrier.wait()
            if (new_content := Vessel.withdraw(vessel_id=vessel_id, amount=amount)) == 1:
                self.stdout.write(f"Successfully withdrawn {amount}kg refrigerant.")
            elif new_content == 0:
                self.stdout.write(f"Vessel with id={vessel_id} not found in the database.")
            else:
                self.stdout.write("Not enough content to withdraw 10 kg")

        def user2():
            barrier.wait()
            if (new_content := Vessel.withdraw(vessel_id=vessel_id, amount=amount)) == 1:
                self.stdout.write(f"Successfully withdrawn {amount}kg refrigerant.")
            elif new_content == 0:
                self.stdout.write(f"Vessel with id={vessel_id} not found in the database.")
            else:
                self.stdout.write("Not enough content to withdraw 10 kg")


        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


        vessel = Vessel.objects.get(id=vessel_id)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
