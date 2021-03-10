from abc import ABC


class RestrictionMeta(type):
    def __repr__(cls):
        return cls.__name__


class Restriction(RestrictionMeta):
    pass


class LibraryRestriction(Restriction):
    pass


class TuitionRestriction(Restriction):
    pass


class AcademicAdvisorRestriction(Restriction):
    pass


class SuspensionRestriction(Restriction):
    pass


class ImmunizationRestriction(Restriction):
    pass
