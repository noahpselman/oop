from src.Entities.EnrollmentObject import EnrollmentObject


class EnrollmentFactory():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if EnrollmentFactory.__instance == None:
            EnrollmentFactory()
        return EnrollmentFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if EnrollmentFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            EnrollmentFactory.__instance = self


    def build_enrollment(self, data):
        enrollment_object = EnrollmentObject(**data)
        print("enrollment object from enrollment factory", enrollment_object.jsonify())
        return enrollment_object

    def build_enrollments(self, data):
        return [self.build_enrollment(row) for row in data]


    