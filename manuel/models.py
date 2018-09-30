from pony.orm import *
from pony.orm.ormtypes import *


db = Database()


class Historic(db.Entity):
    id = PrimaryKey(int, auto=True)
    generation_date = Required(datetime)
    subarea_name = Required(str)
    data = Required(Json)
    report_name = Required(str)
