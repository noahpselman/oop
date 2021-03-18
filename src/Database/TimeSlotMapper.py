from src.Entities.TimeSlot import TimeSlot
from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper


class TimeSlotMapper(Mapper):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TimeSlotMapper.__instance == None:
            TimeSlotMapper()
        return TimeSlotMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TimeSlotMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TimeSlotMapper.__instance = self
        super().__init__()

    def load(self, id: str):
        db_helper = DatabaseHelper.getInstance()
        timeslot_data = db_helper.load_timeslot_by_id(id)
        timeslot_kwargs = {
            'start_time': timeslot_data['starttime'],
            'end_time': timeslot_data['endtime'],
            'days': list(timeslot_data['days'])
        }
        timeslot = TimeSlot(**timeslot_kwargs)
        return timeslot
