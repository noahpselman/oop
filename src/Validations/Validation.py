from __future__ import annotations
from abc import ABC, abstractmethod
from src.Database.DatabaseHelper import DatabaseHelper
from src.util import make_course_index, make_section_index


class Validation(ABC):

    @abstractmethod
    def is_valid(self, student: Student, course_section: CourseSection):
        pass

    # @abstractmethod
    # def on_fail(self, student: Student, course_section: CourseSection):
    #     pass


class PrereqValidation(Validation):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PrereqValidation.__instance == None:
            PrereqValidation()
        return PrereqValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if PrereqValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PrereqValidation.__instance = self

    def is_valid(self, **kwargs):
        """
        required kwargs
        student: Student, course_section: CourseSection
        """
        print("prereq validator doing it's thang")
        student = kwargs['student']
        course_section = kwargs['course_section']
        prereqs = course_section.prereqs
        course_history = [
            c.course_index for c in student.course_history]
        unmet_prereqs = [
            prereq for prereq in prereqs if prereq not in course_history]
        rv = {'validation': self.__class__.__name__,
              'success': not unmet_prereqs,
              'msg': self.__write_msg(unmet_prereqs)}
        return rv

    def __write_msg(self, unmet_prereqs):
        print("unmet_prereqs", unmet_prereqs)
        if not unmet_prereqs:
            return "You have met all the prereqs"
        else:
            return "You have not completed the following prereqs: " + \
                ', '.join(unmet_prereqs)


class StudentRestrictionValidation(Validation):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if StudentRestrictionValidation.__instance == None:
            StudentRestrictionValidation()
        return StudentRestrictionValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if StudentRestrictionValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            StudentRestrictionValidation.__instance = self

    def is_valid(self, **kwargs):
        print("student restriction validator doing its thang")
        student = kwargs['student']
        rv = {'validation': self.__class__.__name__,
              'success': not student.restrictions,
              'msg': self.__write_msg(student.restrictions)}
        return rv

    def __write_msg(self, restrictions):
        print("restrictions", restrictions)
        if not restrictions:
            return "You have no restrictions"
        else:
            return "You have the following restrictions on your account: " + \
                ', '.join(restrictions)


class TimeSlotValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TimeSlotValidation.__instance == None:
            TimeSlotValidation()
        return TimeSlotValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if TimeSlotValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TimeSlotValidation.__instance = self

    def is_valid(self, **kwargs):
        print("time slot validator doing its thang")
        student = kwargs['student']
        course_section = kwargs['course_section']
        current_courses = student.load_courses_by_quarter(
            course_section.quarter)
        overlaps = [c.course_section_name for c in current_courses if not c.timeslot.no_overlap(
            course_section.timeslot)]
        rv = {
            'validation': self.__class__.__name__,
            'success': not overlaps,
            'msg': self.__write_msg(overlaps)
        }

        return rv

    def __write_msg(self, overlaps):
        print("overlaps", type(overlaps))
        if not overlaps:
            return "You have no time conflicts"
        else:
            return "The following coures are causing time conflicts: " + \
                ', '.join(overlaps)


class NotInCourseValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AlreadyInCourseValidation.__instance == None:
            AlreadyInCourseValidation()
        return AlreadyInCourseValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if AlreadyInCourseValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AlreadyInCourseValidation.__instance = self

    def is_valid(self, **kwargs):
        print("already enrolled validator doing its thang")
        student = kwargs['student']
        course_section = kwargs['course_section']
        current_courses = student.load_courses_by_quarter(
            course_section.quarter)
        already_enrolled = False
        for course in current_courses:
            if course.course_section_name == course_section.course_section_name:
                already_enrolled = True
        if already_enrolled:
            msg = "You are already enrolled in this course"
        else:
            msg = "You're not already enrolled in this course"
        rv = {
            'validation': self.__class__.__name__,
            'success': not already_enrolled,
            'msg': msg
        }

        return rv


class InstructorPermissionValidator(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if InstructorPermissionValidator.__instance == None:
            InstructorPermissionValidator()
        return InstructorPermissionValidator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if InstructorPermissionValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InstructorPermissionValidator.__instance = self

    def is_valid(self, **kwargs):
        print("instructor permission validator doing its thang")
        course_section = kwargs['course_section']

        rv = {'validator': self.__class__.__name__}

        if not course_section.instructor_permission_required:
            rv['success'] = True
            rv['msg'] = "Instructor permission is not required for this class"
        else:
            rv['success'] = False
            rv['msg'] = "Instructor permission is required for this class"

        return rv


class OverloadPermissionValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if OverloadPermissionValidation.__instance == None:
            OverloadPermissionValidation()
        return OverloadPermissionValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if OverloadPermissionValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            OverloadPermissionValidation.__instance = self

    def is_valid(self, **kwargs):
        print("overload permission validator doing its thang")
        student = kwargs['student']

        rv = {'validator': self.__class__.__name__}

        if student.max_enrollment <= len(student.current_courses):
            rv['success'] = False
            rv['msg'] = "You are at your maximum enrollment.  An overload request from your department head is required."
        else:
            rv['success'] = True
            rv['msg'] = "You will not exceed your maximum number of enrolled courses"
        return rv


class CourseOpenEnrollmentValidator(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseOpenEnrollmentValidator.__instance == None:
            CourseOpenEnrollmentValidator()
        return CourseOpenEnrollmentValidator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseOpenEnrollmentValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseOpenEnrollmentValidator.__instance = self

    def is_valid(self, **kwargs):
        print("course open enrollment validator doing its thang")
        course_section = kwargs['course_section']

        rv = {'validator': self.__class__.__name__,
              'success': course_section.enrollment_open}

        if course_section.enrollment_open:
            msg = "Course is open for enrollment"
        else:
            msg = "Course is not open for enrollment"
        rv['msg'] = msg

        return rv


class CourseHasEmptySeatValidator(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseHasEmptySeatValidator.__instance == None:
            CourseHasEmptySeatValidator()
        return CourseHasEmptySeatValidator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseHasEmptySeatValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseHasEmptySeatValidator.__instance = self

    def is_valid(self, **kwargs):
        print("course open enrollment validator doing its thang")
        course_section = kwargs['course_section']

        rv = {'validator': self.__class__.__name__}

        if course_section.get_enrollment_total() < course_section.capacity:
            rv['success'] = True
            rv['msg'] = "Course has an open seat"
        else:
            rv['success'] = False
            rv['msg'] = "Course is full"

        return rv


class AlreadyInCourseValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AlreadyInCourseValidation.__instance == None:
            AlreadyInCourseValidation()
        return AlreadyInCourseValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if AlreadyInCourseValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AlreadyInCourseValidation.__instance = self

    def is_valid(self, **kwargs):
        print("already enrolled validator doing its thang")
        student = kwargs['student']
        course_section = kwargs['course_section']
        current_courses = student.load_courses_by_quarter(
            course_section.quarter)
        already_enrolled = False
        for course in current_courses:
            if course.course_section_name == course_section.course_section_name:
                already_enrolled = True
        if already_enrolled:
            msg = "You are already enrolled in this course"
        else:
            msg = "You're not already enrolled in this course"
        rv = {
            'validation': self.__class__.__name__,
            'success': already_enrolled,
            'msg': msg
        }

        return rv


class CourseHasNotStartedValidator(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseHasNotStartedValidator.__instance == None:
            CourseHasNotStartedValidator()
        return CourseHasNotStartedValidator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseHasNotStartedValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseHasNotStartedValidator.__instance = self

    def is_valid(self, **kwargs):
        print("course has not started validator doing its thang")
        course_section = kwargs['course_section']

        rv = {'validator': self.__class__.__name__,
              'success': course_section.state == 'PRESTART'}
        if course_section.state == 'PRESTART':
            msg = "Course is has not started and can be dropped"
        else:
            msg = "Course is has started and cannot be dropped"
        rv['msg'] = msg

        return rv
