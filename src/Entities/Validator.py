from __future__ import annotations


class Validator():
    """
    maybe make this a signleton
    """

    def __init__(self, student: Student, course_section: CourseSection) -> None:
        self.student = student
        self.course_section = course_section

    def check_for_failures(self, validations: List[Validation]):
        print("check for failures called on validator")
        details = {}
        successes = []
        for validation in validations:
            val = validation.getInstance()
            detail = val.is_valid(student=self.student,
                                  course_section=self.course_section)
            print("detail")
            # success = detail[str(validation.__name__)]['success']
            details[validation.__name__] = detail[validation.__name__]
            successes.append(detail[validation.__name__]['success'])
        success = all(successes)
        report = {
            'success': success,
            'details': details
        }
        return report
