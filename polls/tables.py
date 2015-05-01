import django_tables2 as tables
import itertools
class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name

class NameTable(tables.Table):
    amend = CheckBoxColumnWithName(verbose_name="Amend", accessor="netID")
    netID = tables.Column()
    name = tables.Column()
    year = tables.Column()


class SimpleTable(tables.Table):
    Amend = CheckBoxColumnWithName(verbose_name="Select", accessor="netID")
    netID = tables.Column()
    name = tables.Column()
    year = tables.Column()

    def __init__(self, *args, **kwargs):
        super(SimpleTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

  
# table = SimpleTable([{'age': 31, 'id': 10}, {'age': 34, 'id': 11}])
# for cell in table.rows[0]:
#     print cell