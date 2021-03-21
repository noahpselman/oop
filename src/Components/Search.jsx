import React, { Component } from "react";

class Search extends Component {
  state = {
    searchInstructor: "",
    searchDepartment: "",
    searchCourseNumber: "",
  };
  render() {
    return (
      <div className="section">
        <div id="search-container">
          <div id="search-section-heading-container">
            <p className="section-header"> Search</p>
            <p id="search-quarter">
              Search Quarter: {this.props.currentQuarter}
            </p>
          </div>
          <form
            id="search-form"
            onSubmit={(e) =>
              this.props.onSubmit(e, {
                department: this.state.searchDepartment,
                instructor: this.state.searchInstructor,
                courseNumber: this.state.searchCourseNumber,
              })
            }
          >
            <input
              onChange={this.handleSearchDepartmentChange}
              type="text"
              value={this.state.searchDepartment}
              placeholder="Department"
            ></input>
            <input
              onChange={this.handleSearchCourseNumberChange}
              type="text"
              value={this.state.searchCourseNumber}
              placeholder="Course Number"
            ></input>
            <input
              onChange={this.handleSearchInstructorChange}
              type="text"
              value={this.state.searchInstructor}
              placeholder="Instructor"
            ></input>
            <button type="submit">Submit</button>
          </form>
        </div>
        {this.props.searchResults}
      </div>
    );
  }
  handleSearchDepartmentChange = (e) => {
    e.preventDefault();
    this.setState({ searchDepartment: e.target.value });
  };
  handleSearchCourseNumberChange = (e) => {
    e.preventDefault();
    this.setState({ searchCourseNumber: e.target.value });
  };
  handleSearchInstructorChange = (e) => {
    e.preventDefault();
    this.setState({ searchInstructor: e.target.value });
  };
}

export default Search;
