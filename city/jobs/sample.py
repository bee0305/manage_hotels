from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "Test just jon in sample file."

    def execute(self):
        # executing empty sample job
        with open('./info_city.txt','a') as fh:
                    fh.write('some text')
