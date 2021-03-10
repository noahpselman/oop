from datetime import datetime
from src.Entities.Quarter import Quarter


def get_current_quarter():
    from src.Database.DatabaseHelper import DatabaseHelper
    today = datetime.date(datetime.now())
    db_helper = DatabaseHelper.getInstance()
    quarter_data = db_helper.get_current_quarter(today)
    return Quarter(**quarter_data).name


def get_past_quarters():
    from src.Database.DatabaseHelper import DatabaseHelper
    today = datetime.date(datetime.now())
    db_helper = DatabaseHelper.getInstance()
    quarters_data = db_helper.get_past_quarters(today)
    quarters = tuple(
        [Quarter(**quarter_data).name for quarter_data in quarters_data])
    print(quarters)
    return quarters
    # print(quarters)
    # return quarters


def make_course_index(**kwargs):
    """
    course_id: str
    department: str
    """
    dept = kwargs['department']
    id = kwargs['course_id']
    return f"{dept} {id}"


def make_section_index(**kwargs):
    """
    course_id: str
    department: str
    section_number: str
    quarter: str
    """
    dept = kwargs['department']
    id = kwargs['course_id']
    sect_id = kwargs['section_number']
    quarter = kwargs['quarter']
    return f"{dept} {id}/{sect_id}, {quarter}"
