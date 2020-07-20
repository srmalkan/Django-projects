from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'rename django project'

    def add_arguments(self, parser):
        parser.add_argument('newprojectname', type=str,help=help)
        
    def handle(self, *args, **options):
        newprojectname = options['newprojectname']
        files_to_rename = ['boilerPlate\settings\Base.py','boilerPlate\wsgi.py','manage.py']
        folder_to_rename = 'boilerPlate'

        for f in files_to_rename:
            with open(f,'r') as file:
                filedata  = file.read()
            
            filedata = filedata.replace('boilerPlate',newprojectname)
            with open(f,'w') as file:
                file.write(filedata)

        os.rename(folder_to_rename,newprojectname)

        self.stdout.write(self.style.SUCCESS('sucessfully changed'))