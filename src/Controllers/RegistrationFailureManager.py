from __future__ import annotations
from src.Controllers.SearchManager import SearchManager


class RegistrationFailureManager():
    """
    some validations require search results to be returned
    upon failure
    this class is responsible for handling that
    # TODO
    the best thing to do would be to have those policies have
    and "on_fail" method so that this class doesn't need to know
    what to do in each case
    but, i don't think this is the worse solution - there are only
    a couple cases and this way the failure code is all in the same
    place so return value formats can be standardized
    """
    # searching via the controller limits
    search_manager = SearchManager.getInstance()

    def __init__(self) -> None:
        pass

    def execute(self, *, course_section: CourseSection, report: ValidationReport):

        # only one search result retrieved
        # timeslot conflict gets priority
        if report.timeslot_conflict:
            search_type = "time_conflict"
            search_results = self.__handleTimeFail(course_section)
        elif report.needs_lab:
            search_type = "lab"
            search_results = self.__handleLabFail(course_section)
        else:
            search_type = ""
            search_results = []

        return {"search_type": search_type, "search_results": search_results}

    def __handleLabFail(self, course_section: CourseSection):

        search_result = self.search_manager.execute({
            'quarter': course_section.quarter,
            'course_id': course_section.lab.course_id})
        return search_result

    def __handleTimeFail(self, course_section: CourseSection):
        search_result = self.search_manager.execute({
            'quarter': course_section.quarter,
            'course_id': course_section.course_id})
        return search_result
