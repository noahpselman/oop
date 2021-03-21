import React from "react";
import "./App.css";
import CurrentCourses from "./Components/CurrentCourses";
import LoginForm from "./Components/LoginForm";
import NavBar from "./Components/NavBar";
import Popup from "./Components/Popup";
import PopupContent from "./Components/PopupContent";
import Restrictions from "./Components/Restrictions";
import Search from "./Components/Search";
import StudentInfo from "./Components/StudentInfo";
// import LoginForm from './Components/LoginForm'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: false,
      userId: "",
      password: "",
      entityData: {},
      entityDataLoaded: false,
      entityType: "",
      currentQuarter: "",
      displayCourses: "",
      searchInstructor: "",
      searchDepartment: "",
      searchCourseNumber: "",
      searchResult: [],
      resultsFound: false,
      popupMessage: [],
      showPopup: false,
      popupHeading: "",
      popupButton: "",
      popupSearchResult: [],
      registrationAttemptCourse: "",
    };
    // this.getInitialState()
  }

  handleLoginSubmit = (e, userId, password) => {
    e.preventDefault();
    console.log(`submitting ${userId}`);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, password: password }),
    };
    const url = "/auth";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleIncomingLoginData(data));
  };
  handleLogout = (e) => {
    console.log("handleLogout clicked");
    this.resetState();
  };
  handleIncomingLoginData = (data) => {
    console.log("handleIncomingData called");
    console.log(data);

    const loginSuccess = Boolean(data.loginSuccess);

    if (loginSuccess) {
      this.setState({ loggedIn: true, userId: data.loginSuccess }, () =>
        localStorage.setItem("loggedIn", JSON.stringify(this.state.loggedIn))
      );
      this.loadUser();
    } else {
      console.log("about to reset state");
      this.resetState();
    }
  };

  loadUser = () => {
    console.log(`loadUser called`);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: this.state.userId,
        logged_in: this.state.loggedIn,
      }),
    };
    const url = "/user";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleIncomingUserData(data));
  };

  handleIncomingUserData = (data) => {
    console.log("handle incoming user data called");
    console.log(data);
    this.setInitialState(data);
  };

  setInitialState = (data) => {
    console.log("set user states called");
    this.setState({ entityType: data.entityData.user_data.user_type }, () =>
      localStorage.setItem("entityType", this.state.entityType)
    );
    this.setState({ entityData: data.entityData }, () =>
      localStorage.setItem("entityData", JSON.stringify(this.state.entityData))
    );
    this.setState({ currentQuarter: data.currentQuarter }, () =>
      localStorage.setItem(
        "currentQuarter",
        JSON.stringify(this.state.currentQuarter)
      )
    );
    this.setState(
      { displayCourses: this.state.entityData.current_courses },
      () =>
        localStorage.setItem(
          "displayCourses",
          JSON.stringify(this.state.entityData.current_courses)
        )
    );
    this.setState({ entityDataLoaded: true }, () =>
      localStorage.setItem(
        "entityDataLoaded",
        JSON.stringify(this.state.entityDataLoaded)
      )
    );
  };

  setCourseChangeState = (data) => {
    this.setState({ entityData: data.entityData }, () =>
      localStorage.setItem("entityData", JSON.stringify(this.state.entityData))
    );
    this.requestCurrentCourses();
  };

  handleSearchSubmit = (e, searchCriteria) => {
    console.log("handle search submit called");
    console.log(searchCriteria);
    e.preventDefault();
    // console.log(e.target);
    let queryParams = [`quarter=${this.state.currentQuarter}`];
    if (searchCriteria.instructor) {
      queryParams.push(`instructor=${searchCriteria.instructor}`);
    }
    if (searchCriteria.department) {
      queryParams.push(`department=${searchCriteria.department.toUpperCase()}`);
    }
    if (searchCriteria.courseNumber) {
      queryParams.push(`course_id=${searchCriteria.courseNumber}`);
    }
    queryParams = queryParams.join("&");

    console.log(queryParams);
    const query = "/search?" + queryParams;
    fetch(query)
      .then((res) => res.json())
      .then((data) => this.handleSearchData(data));
  };

  handleSearchData = (data) => {
    console.log("handle search data");
    console.log(data);
    this.setState({
      searchResult: data.searchResult || [],
      resultsFound: data.resultsFound,
    });
  };

  handleCourseDrop = (e) => {
    console.log("handle course drop called");
    console.log(e.target.attributes.sectionIndex.nodeValue);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        logged_in: this.state.loggedIn,
        user_id: this.state.userId,
        section_index: e.target.attributes.sectionIndex.nodeValue,
        entity_data: this.state.entityData,
      }),
    };
    const url = "/drop";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleDropData(data));
  };

  handleCourseRegister = (e) => {
    console.log("handle course registration called");
    console.log(e.target);
    let sectionIndex = e.target.attributes.sectionIndex.nodeValue;
    let instrPermReq =
      e.target.attributes.instructor_permission.nodeValue === "required";
    let overloadReq =
      this.state.entityData.max_enrollment <= this.state.displayCourses.length;
    console.log(sectionIndex, instrPermReq, overloadReq);
    console.log("max enrollment", this.state.entityData.max_enrollment);
    console.log("display courses length", this.state.displayCourses.length);
    let button = "register";
    let msg = `Register for ${sectionIndex}`;
    if (instrPermReq) {
      button = "instrPerm";
      msg = "This course requires instructor permission";
    } else if (overloadReq) {
      button = "overload";
      msg = "Before you register for this course you must request to overload";
    }
    console.log(button);

    this.setState({
      registrationAttemptCourse: sectionIndex,
      popupMessage: [msg],
      popupHeading: "Course Registration Attempt",
      popupSearchResult: [],
      popupButton: button,
      showPopup: true,
    });
    // show pop up
    // respond to popup buttons
  };

  requestLab = (e) => {
    e.preventDefault();
    console.log("handle request lab hit");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: this.state.userId,
        section_index: this.state.registrationAttemptCourse,
        lab_index: e.target.attributes.sectionIndex.nodeValue,
      }),
    };
    const url = "/lab";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleRegisterData(data));
    this.resetSearch();
    this.handlePopupClose();
  };

  requestRegister = (e) => {
    e.preventDefault();
    console.log("handle register register block hit");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        logged_in: this.state.loggedIn,
        user_id: this.state.userId,
        section_index: this.state.registrationAttemptCourse,
        entity_data: this.state.entityData,
      }),
    };
    const url = "/register";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleRegisterData(data));
    this.resetSearch();
    this.handlePopupClose();
  };

  resetSearch = () => {
    this.setState({ resultsFound: false, searchResult: [] });
  };

  handleRegisterData = (data) => {
    console.log("data from register", data);
    console.log(data);
    if (data.report.db_updated && data.report.success) {
      console.log("about to set state from handle register data");
      this.setCourseChangeState(data);
    } else {
      this.setRegFailPopup(data);
    }
  };

  setRegFailPopup = (data) => {
    console.log("reg fail popup called");
    console.log(data);

    if (data.searchType) {
      console.log("there is a search type son");
      let msg;
      let heading;
      switch (data.searchType) {
        case "lab":
          msg = "You must first enroll in a lab";
          heading = "Choose a Lab";
          break;
        case "time_conflict":
          msg = "Choose a section at a different time";
          heading = "Time Conflict";
          break;
      }
      console.log("search result", data.searchResult);
      console.log("State", this.state);
      this.setState({
        showPopup: true,
        popupMessage: [msg],
        popupSearchResult: data.searchResult,
        popupButton: "none",
        popupHeading: heading,
      });
    } else {
      this.setState({
        showPopup: true,
        popupMessage: data.report.msgs,
        popupSearchResult: [],
        popupButton: "none",
        popupHeading: "Registration Attempt Failed",
      });
    }
  };

  handleDropData = (data) => {
    console.log("handle drop data called");
    console.log(data);
    if (data.report.db_updated && data.report.success) {
      this.setCourseChangeState(data);
    } else {
      // this.setPopupData(data)
    }
  };

  // console.log(this.state.entityType)
  resetState = () => {
    console.log("resetting state and localStorage");
    localStorage.clear();
    this.setState({
      loggedIn: false,
      entityType: "",
      entityData: {},
      entityDataLoaded: false,
      userId: "",
      password: "",
      showPopup: false,
      popupHeading: "",
      popupMessage: [],
      popupButton: "",
      popupSearchResult: [],
    });
  };

  handlePopupClose = () => {
    this.setState({
      showPopup: false,
      popupHeading: "",
      popupMessage: [],
      popupButton: "",
      popupSearchResult: [],
    });
  };

  handleQuarterChange = (e) => {
    e.preventDefault();
    console.log("handle quarter change");
    console.log(e.target.value);
    this.setState(
      { currentQuarter: e.target.value },
      this.requestCurrentCourses
    );
  };

  requestCurrentCourses = () => {
    localStorage.setItem(
      "currentQuarter",
      JSON.stringify(this.state.currentQuarter)
    );
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: this.state.userId,
        quarter: this.state.currentQuarter,
      }),
    };
    const url = "/currentcourses";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleNewCurrentCourses(data));
  };

  handleNewCurrentCourses = (data) => {
    console.log("handle new current courses called");
    console.log(data);
    this.setState({ displayCourses: data.courses });
  };

  handleInstructorPermission = (e) => {
    console.log("handle instructor permission pressed");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: this.state.userId,
        section_index: this.state.registrationAttemptCourse,
        permission_type: "instructor",
      }),
    };
    const url = "/permission";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleIncomingPermissionResponse(data));
  };

  handleIncomingPermissionResponse = (data) => {
    console.log("permission response data", data);
    this.setState({
      popupShow: true,
      popupMessage: [
        `Permission request ${data.success ? "successful" : "unsuccessful"}.`,
      ],
      popupSearchResult: [],
      popupButton: "none",
      popupHeading: "Permission Request",
    });
    this.requestCurrentCourses();
  };

  handleOverloadRequest = (e) => {
    console.log("handle overload request clicked");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: this.state.userId,
        section_index: this.state.registrationAttemptCourse,
        permission_type: "overload",
      }),
    };
    const url = "/permission";
    fetch(url, requestOptions)
      .then((res) => res.json())
      .then((data) => this.handleIncomingPermissionResponse(data));
  };

  buildSearch = (list, clickFunction) => {
    let searchResult = list.map((course) => {
      let registerButton = <div></div>;
      let open =
        course.enrollment_open && course.enrollment_count < course.capacity;

      if (open) {
        registerButton = (
          <div
            className="register-button"
            instructor_permission={
              course.instructor_permission_required
                ? "required"
                : "not required"
            }
            sectionIndex={course.section_index}
            onClick={clickFunction}
          >
            Register
          </div>
        );
      }
      return (
        <div className="search-result-item">
          <div className="course-info">
            <div className="course-data">
              <p>{course.course.name}</p>
              <p>{course.section_index}</p>
            </div>
            <div className="other-course-data">
              <p>Instructor: {course.instructor.user_data.full_name}</p>
              <p>
                {course.timeslot.start_time}-{course.timeslot.end_time}{" "}
                {course.timeslot.days}
              </p>
            </div>
          </div>
          <div className="course-enrollment">
            <div className="enrollment-info">
              <p>
                Enrollment: {course.enrollment_count} / {course.capacity}
              </p>
              <p>Prerequisites: {course.course.prereqs.join(", ")}</p>
              <p>
                {course.instructor_permission_required
                  ? "Instructor Permission Required"
                  : ""}
              </p>
            </div>
            <div className="register-holder">
              <p className="enrollment-open-label">
                {open ? "Open" : "Closed"}
              </p>
              {registerButton}
            </div>
          </div>
        </div>
      );
    });

    let searchResults = (
      <div className="section" id="search-result-container">
        {searchResult}
      </div>
    );
    return searchResults;
  };

  render = () => {
    console.log("state in render", this.state);
    let userData = <div></div>;
    let loginForm = <div></div>;
    let currentCourses = <div></div>;
    let currentCourse = <div></div>;
    let restrictions = <div></div>;
    let logoutButton = <div></div>;
    let search = <div></div>;
    let popup = <div style={{ display: "none" }}></div>;
    // let searchResult = <div></div>
    let searchResults = <div></div>;
    let popupButton = <div></div>;

    if (this.state.loggedIn && this.state.entityDataLoaded) {
      logoutButton = (
        <div
          id="logout-button"
          className="navbar-item"
          onClick={this.handleLogout}
        >
          Logout
        </div>
      );
    }

    return (
      <div id="global-wrapper">
        {/* {popup} */}
        <NavBar onClick={this.handleLogout} loggedIn={this.state.loggedIn} />
        <div id="content-wrapper">
          {this.state.showPopup ? (
            <Popup
              popupButton={this.buildPopupButton()}
              popupHeading={this.state.popupHeading}
              onClose={this.handlePopupClose}
            >
              <PopupContent
                popupContent={this.state.popupMessage.map((item) => (
                  <li>{item}</li>
                ))}
                popupSearchResultContent={this.buildSearch(
                  this.state.popupSearchResult,
                  this.requestLab
                )}
              />
            </Popup>
          ) : (
            <div></div>
          )}
          {this.state.entityDataLoaded ? (
            <div>
              <StudentInfo entityData={this.state.entityData} />
              <Restrictions restrictions={this.state.entityData.restrictions} />
              <CurrentCourses
                handleQuarterChange={this.handleQuarterChange}
                onCourseDrop={this.handleCourseDrop}
                displayCourses={this.state.displayCourses}
                currentQuarter={this.state.currentQuarter}
              />
              <Search
                currentQuarter={this.state.currentQuarter}
                searchResultsFound={this.state.searchResultsFound}
                searchResults={this.buildSearch(
                  this.state.searchResult,
                  this.handleCourseRegister
                )}
                onSubmit={this.handleSearchSubmit}
              />
            </div>
          ) : (
            <LoginForm onSubmit={this.handleLoginSubmit} />
          )}

          {/* <div>{searchResults}</div> */}
        </div>
      </div>
    );
  };

  buildPopupButton() {
    let popupButton = <div></div>;
    switch (this.state.popupButton) {
      case "register":
        popupButton = (
          <div className="popup-button" onClick={this.requestRegister}>
            Register
          </div>
        );
        break;
      case "instrPerm":
        popupButton = (
          <div
            className="popup-button"
            onClick={this.handleInstructorPermission}
          >
            Request Instructor Permission
          </div>
        );
        break;
      case "overload":
        popupButton = (
          <div className="popup-button" onClick={this.handleOverloadRequest}>
            Request Overload
          </div>
        );
        break;
    }
    return popupButton;
  }
}

export default App;
