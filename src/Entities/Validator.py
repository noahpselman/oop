from __future__ import annotations
from src.Validations.Validation import AlreadyInCourseValidation, CourseHasEmptySeatValidator, CourseHasNotStartedValidator, CourseOpenEnrollmentValidator, InstructorPermissionValidator, NotInCourseValidation, OverloadPermissionValidation, PrereqValidation, StudentRestrictionValidation, TimeSlotValidation


class Validator():
    """
    maybe make this a signleton
    """
    REGISTER_VALIDATIONS = ([
        PrereqValidation,
        StudentRestrictionValidation,
        TimeSlotValidation,
        NotInCourseValidation,
        InstructorPermissionValidator,
        OverloadPermissionValidation,
        CourseOpenEnrollmentValidator,
        CourseHasEmptySeatValidator
    ])

    DROP_VALIDATIONS = ([
        AlreadyInCourseValidation,
        CourseHasNotStartedValidator
    ])

    def __init__(self, student: Student, course_section: CourseSection) -> None:
        self.student = student
        self.course_section = course_section

    def check_for_failures(self, validations: List[Validation]):
        print("check for failures called on validator")
        details = []
        for validation in validations:
            val = validation.getInstance()
            detail = val.is_valid(student=self.student,
                                  course_section=self.course_section)
            details.append(detail)
        success = all([r['success'] for r in details])
        report = {
            'success': success,
            'details': details
        }
        return report
