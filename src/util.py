from datetime import datetime
from src.Entities.Quarter import Quarter


def get_current_quarter():
    from src.Database.DatabaseHelper import DatabaseHelper
    today = datetime.date(datetime.now())
    db_helper = DatabaseHelper.getInstance()
    quarter_data = db_helper.load_current_quarter(today)
    return Quarter(**quarter_data).name


def get_past_quarters():
    from src.Database.DatabaseHelper import DatabaseHelper
    today = datetime.date(datetime.now())
    db_helper = DatabaseHelper.getInstance()
    quarters_data = db_helper.load_past_quarters(today)
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


def parse_section_index(section_index: str):
    """
    example section index: TRFG 441/1, WINTER 2021
    returns dict with separate components of section
    index as keys:
        department: TRFG
        course_id: 441
        quarter: WINTER 2021
        section_number: 1
    """
    rv = {
        'department': section_index[:4],
        'course_id': section_index[5:8],
        'section_number': section_index[section_index.find(
            '/')+1:section_index.find(',')],
        'quarter': section_index[-11:]  # each quarter is 11 characters
    }
    return rv


def get_system_email():
    return "fake_email@oop_project.100"
