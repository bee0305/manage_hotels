from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "Test from hourly dir."

    def execute(self):
        # executing empty sample job
        print("greet from smaple2.py hourly")
