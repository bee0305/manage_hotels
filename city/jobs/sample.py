from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "Test just jon in sample file."

    def execute(self):
        # executing empty sample job
        print("here i am")
