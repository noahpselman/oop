import React, { Component } from "react";

class CurrentCourses extends Component {
  state = {};

  render() {
    let currentCourse = this.props.displayCourses.map((course) => {
      return (
        <div className="course-container">
          <div className="course-info">
            <div>
              <p>{course.course.name}</p>
              <p>{course.course.course_index}</p>
            </div>
            <div>
              <p>Instructor: {course.instructor.user_data.full_name}</p>
              <p>
                {course.timeslot.start_time}-{course.timeslot.end_time}{" "}
                {course.timeslot.days}
              </p>
            </div>
          </div>
          <div className="course-enrollment">
            <div className="enrollment-info">
              {/* <p>Enrollment Status {course}</p> */}
              <p>
                Enrollment: {course.enrollment_count} / {course.capacity}
              </p>
            </div>
            <div className="drop-holder">
              <div
                className="drop-button"
                sectionIndex={course.section_index}
                onClick={this.props.onCourseDrop}
              >
                Drop
              </div>
            </div>
          </div>
        </div>
      );
    });

    return (
      <div className="section">
        <div id="current-courses-headline">
          <p className="section-header">Current Course</p>
          <p className="section-header">
            Currently Displaying: {this.props.currentQuarter}
          </p>
          <div id="quarter-select-holder">
            <p id="quarter-dropdown-label">Change Quarter: </p>
            <select
              id="quarter-dropdown"
              onChange={this.props.handleQuarterChange}
            >
              <option value="AUTUMN 2020">AUTUMN 2020</option>
              <option value="WINTER 2021">WINTER 2021</option>
              <option value="SPRING 2021">SPRING 2021</option>
            </select>
          </div>
        </div>
        <p>Note: Some enrollments may be tentative or pending</p>
        {currentCourse}
      </div>
    );
  }
}

export default CurrentCourses;
