class ValidationReport():
    """
    data structure that holds data on how a registration attempt went
    """

    def __init__(self):

        self._data = {}
        self._fails = []
        self._msgs = []
        self._is_successful = True

        self._db_updated = False

    def jsonify(self):
        result = {
            'data': self._data,
            'fails': self._fails,
            'success': self._is_successful,
            'db_updated': self._db_updated,
            'msgs': self._msgs
        }
        return result

    @property
    def db_updated(self):
        return self._db_updated

    @db_updated.setter
    def db_updated(self, new_db_updated):
        self._db_updated = new_db_updated

    @property
    def is_successful(self):
        return self._is_successful

    def add_data(self, *, validation: str, success: bool, msg: str):
        report_line = {
            'success': success,
            'msg': msg
        }
        self._data[validation] = report_line
        if not success:
            self._is_successful = False
            self._fails.append(validation)
            self._msgs.append(msg)


class DropValidationReport(ValidationReport):
    def __init__(self):
        super().__init__()


class RegisterValidationReport(ValidationReport):
    def __init__(self):
        super().__init__()
        self._needs_lab = False
        self._needs_instructor_permission = False
        self._needs_overload_permission = False
        self._timeslot_conflict = False

    @property
    def needs_overload_permission(self):
        return self._needs_overload_permission

    @property
    def needs_instructor_permission(self):
        return self._needs_instructor_permission

    @property
    def needs_lab(self):
        return self._needs_lab

    @property
    def timeslot_conflict(self):
        return self._timeslot_conflict

    def add_data(self, *, validation: str, success: bool, msg: str):
        super().add_data(validation=validation, success=success, msg=msg)
        self.__update_attributes(validation, success)

    def __update_attributes(self, validation: str, success: bool):
        if not success:

            if validation == 'LabValidation':
                self._needs_lab = True
            elif validation == 'InstructorPermissionValidation':
                self._needs_instructor_permission = True
            elif validation == 'OverloadPermissionValidation':
                self._needs_overload_permission = True
            elif validation == 'TimeSlotValidation':
                self._timeslot_conflict = True

    def jsonify(self):
        result = super().jsonify()
        result['needs_lab'] = self._needs_lab
        result['needs_instructor_permission'] = self._needs_instructor_permission
        result['needs_overload_permission'] = self._needs_overload_permission
        result['timeslot_conflict'] = self._timeslot_conflict

        return result
