import csv
from dateutil.parser import parse

from deals.models import Deal, User, Gem


def read_csv_data(path):
    with open(
        path,
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
        except (Gem.DoesNotExist, User.DoesNotExist) as error:
            return str(error)
        except UnicodeDecodeError:
            return 'Only UTF-8 encoding available'
