import csv
import threading

from dateutil.parser import parse

from deals.models import Deal, Gem, User


class ReadCSV(threading.Thread):
    """
    Uploading data from deals.csv to database.
    """

    result = None

    def __init__(self, path):
        super(ReadCSV, self).__init__()
        self.path = path

    def run(self):
        with open(
            self.path,
            encoding='utf-8'
        ) as csvfile:
            try:
                csvfile.readline()
                deals = csv.reader(csvfile)
                Deal.objects.all().delete()
                for deal in deals:
                    (
                        username, gem_name, total, quantity, date
                    ) = (
                        deal[0], deal[1], deal[2], deal[3], deal[4]
                    )
                    customer = User.objects.get(username=username)
                    item = Gem.objects.get(gem_name=gem_name)
                    Deal.objects.get_or_create(
                        customer=customer,
                        item=item,
                        total=total,
                        quantity=quantity,
                        date=parse(date)
                    )
            except (Gem.DoesNotExist, User.DoesNotExist, ValueError) as error:
                self.result = str(error)
            except IndexError:
                self.result = 'Only (customer,item,total,quantity,date) data available'
            except (UnicodeDecodeError):
                self.result = 'Only UTF-8 encoding available'
