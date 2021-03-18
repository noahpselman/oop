from __future__ import annotations
from src.Email.Emailer import Emailer
from src.Database.EnrollmentObjectMapper import EnrollmentObjectMapper
from src.Database.DatabaseHelper import DatabaseHelper
from types import resolve_bases
from src.Entities.CourseSection import CourseSection
# from src.Factories.RequestFactory import RequestFactory
from src.util import parse_section_index
from src.Entities.Request import InstructorPermissionRequest, OverloadPermissionRequest


class RequestManager():
    """
    singleton
    responsible for executing varieties of permission requests
    """
    __instance = None

    REQUESTS = {
        'INSTRUCTOR_PERMISSION': InstructorPermissionRequest,
        'OVERLOAD_PERMISSION': OverloadPermissionRequest
    }

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RequestManager.__instance == None:
            RequestManager()
        return RequestManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if RequestManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RequestManager.__instance = self

    def request_permission(self, *, 
                        student: Student, course_section: CourseSection, 
                        permission_type:str):
        if permission_type == "instructor":
            result = self.__request_instructor_permission(student=student, course_section=course_section)

        elif permission_type == "overload":
            result = self.__request_overload_permission(student=student, course_section=course_section)

        return result

    def __request_instructor_permission(self, *, 
            student: Student, course_section: CourseSection) -> bool:
        # request = InstructorPermissionRequest(student_id=student.id, course_id=course_section.course_id,
        #                                       department=department, quarter=quarter)
        request = self.__build_request(request_type="INSTRUCTOR_PERMISSION",
                                       student=student,
                                       course_section=course_section)
        success = self.__execute_request(
            student_email=student.email, request=request)

        return success

    def __request_overload_permission(self, *, student: Student, course_section: CourseSection) -> bool:
        request = self.__build_request(request_type="OVERLOAD_PERMISSION",
                                       student=student,
                                       course_section=course_section)
        success = self.__execute_request(
            student_email=student.email, request=request)
        return success

    def __build_request(self, *, request_type: str, student: Student, course_section: CourseSection) -> Request:
        """
        creates request object of appropriate time
        """
        Request = self.REQUESTS[request_type]
        return Request(student=student, course_section=course_section)

    def __execute_request(self, *, student_email: str, request: Request) -> bool:
        """
        executes tangible steps for request
        sends email and saves request
        """

        email_sent = self.send_email(msg=request.msg,
                                     student_email=student_email,
                                     requestee_email=request.recipient_email,
                                     )
        db_success = self.__save_request(request)
        return email_sent and db_success

    def __save_request(self, request) -> bool:
        """
        inserts request into enrollment table
        """
        mapper = EnrollmentObjectMapper.getInstance()
        db_success = mapper.insert(request)
        return db_success

    def send_email(self, *, student_email: str, requestee_email: str, msg: str) -> bool:
        """
        sends email (but not really tho)
        """
        emailer = Emailer.getInstance()
        success = emailer.send(to=[requestee_email, student_email], msg=msg)
        return success
