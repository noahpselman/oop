from __future__ import annotations


class Validator():
    """
    responsible for filling out a validation report by
    checking the "is_valid" method on validation objects
    """

    def __init__(self, student: Student, course_section: CourseSection) -> None:
        self.student = student
        self.course_section = course_section

    def check_for_failures(self, validations: List[Validation], report: ValidationReport):
        """
        notice this method does not return anything,
        it instead populates a validation report with necessary information
        """
        print("check for failures called on validator")

        for validation in validations:
            val = validation.getInstance()
            val.is_valid(report, student=self.student,
                         course_section=self.course_section)
