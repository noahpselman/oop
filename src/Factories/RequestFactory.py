from src.Entities.Request import InstructorPermissionRequest, OverloadPermissionRequest


class RequestFactory():
    __instance = None

    MSG_WRITERS = {
        'INSTRUCTOR_PERMISSION': InstructorPermissionMsgWriter,
        'OVERLOAD_PERMISSION': OverloadPermissionMsgWriter
    }

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RequestFactory.__instance == None:
            RequestFactory()
        return RequestFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if RequestFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RequestFactory.__instance = self

    def build(self, *, request_type: str = request_type, course_id: str = course_id, department: str = department,
              section_number: str = section_number, quarter: str = quarter):

        request = Request(student_id=student_id, quarter=self.quarter,
                          section_number=self.section_number, department=self.department,
                          course_id=self.course_id)
