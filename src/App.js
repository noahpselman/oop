
import React from 'react'
import Modal from './Components/Modal'
import './App.css';
// import LoginForm from './Components/LoginForm'

class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: JSON.parse(localStorage.getItem('loggedIn')) || false,
            userId: localStorage.getItem('userId') || "",
            password: localStorage.getItem('password') || "",
            entityData: JSON.parse(localStorage.getItem('entityData')) || {},
            entityType: localStorage.getItem('entityType') || "",
            searchInstructor: "",
            searchDepartment: "",
            searchCourseNumber: "",
            currentQuarter: "",
            regFail: false,
            popupMessage: [],
            searchResult: {},
            resultsFound: false,
            overloadReqMsg: false,
            instrPermMsg: false
        }
        // this.getInitialState()

    }



    getInitialState = () => {
        console.log("getting initial state")
        this.setState({ entityType: localStorage.getItem('entityType') })
        this.setState({ entityData: JSON.parse(localStorage.getItem('entityData')) })
    }


    handleSearchDepartmentChange = (e) => {
        e.preventDefault();
        this.setState({ searchDepartment: e.target.value })
    }
    handleSearchCourseNumberChange = (e) => {
        e.preventDefault();
        this.setState({ searchCourseNumber: e.target.value })
    }
    handleSearchInstructorChange = (e) => {
        e.preventDefault();
        this.setState({ searchInstructor: e.target.value })
    }
    handleUsernameChange = (e) => {
        e.preventDefault();
        this.setState({ userId: e.target.value },
            () => { localStorage.setItem('userId', e.target.value) })
    }
    handlePasswordChange = (e) => {
        e.preventDefault();
        this.setState({ password: e.target.value },
            () => { localStorage.setItem('password', e.target.value) })
    }
    handleLoginSubmit = (e) => {

        e.preventDefault();
        console.log(`submitting ${this.state.user_id}`)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: this.state.userId, password: this.state.password })
        };
        const url = '/auth'
        fetch(url, requestOptions)
            .then(res => res.json())
            .then(data => this.handleIncomingLoginData(data))
    }
    handleLogout = (e) => {
        console.log("handleLogout clicked")
        this.resetState()
    }
    handleIncomingLoginData = (data) => {
        console.log('handleIncomingData called')
        console.log(data)

        const loginSuccess = data.loginSuccess
        if (loginSuccess) {
            console.log("set user state called")
            this.setUserStates(data)
        }
        else {
            this.resetState()
        }
    }

    setUserStates = (data) => {
        this.setState({ entityType: data.entityData.user_data.user_type },
            () => localStorage.setItem('entityType', this.state.entityType))
        this.setState({ entityData: data.entityData },
            () => localStorage.setItem('entityData', JSON.stringify(this.state.entityData)))
        this.setState({ loggedIn: true },
            () => localStorage.setItem('loggedIn', true))
    }

    handleSearchSubmit = (e) => {
        console.log("handle search submit called")
        e.preventDefault()
        console.log(e.target)
        let queryParams = []
        if (this.state.searchInstructor) {
            queryParams.push(`instructor=${this.state.searchInstructor}`)
        }
        if (this.state.searchDepartment) {
            queryParams.push(`department=${this.state.searchDepartment}`)
        }
        if (this.state.searchCourseNumber) {
            queryParams.push(`course_id=${this.state.searchCourseNumber}`)
        }
        queryParams = queryParams.join('&')

        console.log(queryParams)
        const query = '/search?' + queryParams
        fetch(query)
            .then(res => res.json())
            .then(data => this.handleSearchData(data))
    }

    handleSearchData = (data) => {
        console.log(data)
        this.setState({ searchResult: data.searchResult })
        this.setState({ resultsFound: data.resultsFound })
    }

    handleCourseDrop = (e) => {
        console.log("handle course drop called")
        console.log(e.target.attributes.sectionIndex.nodeValue)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                logged_in: this.state.loggedIn,
                user_id: this.state.userId,
                section_index: e.target.attributes.sectionIndex.nodeValue,
                entity_data: this.state.entityData
            })
        };
        const url = '/drop'
        fetch(url, requestOptions)
            .then(res => res.json())
            .then(data => this.handleDropData(data))
    }





    handleCourseRegister = (e) => {
        console.log("handle course registration called")
        // this.setState({currentRegisterCourse: e.target.attributes.attri})
        if (this.state.entityData.current_courses.length > this.state.entityData.max_enrollment) {

            this.setState({
                overloadReqMsg: true,
                popupMessage: ["Registering for another course will require you to request overload permission"]
            })
        }
        else if (e.target.attributes.instrPerm) {
            console.log('instr perm clause')
            this.setState({
                instrPermMsg: true,
                popupMessage: ["To register for this class you must request instructor permission"]
            })
        }
        else {
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    logged_in: this.state.loggedIn,
                    user_id: this.state.userId,
                    section_index: e.target.attributes.sectionIndex.nodeValue,
                    entity_data: this.state.entityData
                })
            };
            const url = '/register'
            fetch(url, requestOptions)
                .then(res => res.json())
                .then(data => this.handleRegisterData(data))
            this.resetSearch()
        }


    }

    resetSearch = () => {
        this.setState({ resultsFound: false, searchResult: {} })
    }

    handleRegisterData = (data) => {
        console.log(data)
        if (data.report.db_updated && data.report.success) {
            this.setUserStates(data)
        }
        else {
            this.setPopupData(data)
        }
    }

    handleDropData = (data) => {
        console.log("handle drop data called")
        console.log(data)
        if (data.report.db_updated && data.report.success) {
            this.setUserStates(data)
        }
        else {
            this.setPopupData(data)


        }
    }

    setPopupData = (data) => {
        let fails = data.report.details.filter((item) => {
            return !item.success
        }).map((item) => {
            return item.msg
        })
        console.log(fails)
        this.setState({ popupMessage: fails })
        this.setState({ regFail: true })
        console.log('popup message state', this.state.popupMesssge)
    }
    // console.log(this.state.entityType)
    resetState = () => {
        console.log("resetting state and localStorage")
        localStorage.clear()
        this.setState({ loggedIn: false })
        this.setState({ entityType: "" })
        this.setState({ entityData: {} })
        this.setState({ userId: "" })
        this.setState({ password: "" })
    }

    handlePopupClose = () => {
        this.setState({ regFail: false })
    }


    render = () => {
        console.log("state in render", this.state)
        let userData = (<div></div>)
        let loginForm = (<div></div>)
        let currentCourses = (<div></div>)
        let currentCourse = (<div></div>)
        let restrictions = (<div></div>)
        let logoutButton = (<div></div>)
        let search = (<div></div>)
        let popup = <div style={{ display: 'none' }}></div>
        let searchResult = <div></div>
        let searchResults = <div></div>

        if (this.state.loggedIn) {
            logoutButton = (
                <div id='logout-button' className="navbar-item" onClick={this.handleLogout}>Logout</div>
            )

            search = (
                <div className="section">
                    < p className="search-header" > Search</p >
                    <form onSubmit={this.handleSearchSubmit}>
                        <input onChange={this.handleSearchDepartmentChange} type="text" value={this.state.searchDepartment} placeholder="Department"></input>
                        <input onChange={this.handleSearchCourseNumberChange} type="text" value={this.state.searchCourseNumber} placeholder="Course Number"></input>
                        <input onChange={this.handleSearchInstructorChange} type="text" value={this.state.searchInstructor} placeholder="Instructor"></input>
                        <button type="submit">Submit</button>
                    </form>
                </div >
            )

            userData = (
                <div id="user-data" className="section">
                    <div className='user-data-element'>
                        <p>Name: {this.state.entityData.user_data.full_name}</p>
                    </div>
                    <div className='user-data-element'>
                        <p>Id: {this.state.entityData.user_data.id}</p>
                    </div>
                </div>
            )

            currentCourse = this.state.entityData.current_courses.map((course) => {
                return (
                    <div className='course-container'>
                        <div className='course-info'>

                            <div>
                                <p>{course.course.name}</p>
                                <p>{course.course.course_index}</p>
                            </div>
                            <div>
                                <p>Instructor: {course.instructor.user_data.full_name}</p>
                                <p>{course.timeslot.start_time}-{course.timeslot.end_time} {course.timeslot.days}</p>

                            </div>
                        </div>
                        <div className="course-enrollment">
                            <div>
                                <p>Enrollment: {course.enrollment_count} / {course.capacity}</p>
                            </div>
                            <div className="drop-button" sectionIndex={course.section_index} onClick={this.handleCourseDrop}>Drop</div>

                        </div>
                    </div>

                )
            })

            currentCourses = (
                <div className="section">
                    Current Course
                    {currentCourse}

                </div>
            )

            let restriction = this.state.entityData.restrictions.map((restriction) => {
                return (
                    <div>
                        <p>{restriction}</p>
                    </div>
                )
            })

            restrictions = (
                <div className="section">
                    <p className="restrictions-heading">Restrictions</p>
                    {restriction}
                </div>
            )


            let instrPermButton = <div></div>
            if (this.state.instrPermMsg) {
                <div className='popup-button' onClick={this.handleOverloadReq}>Request Permission</div>
            }
            let overloadReqButton = <div></div>
            if (this.state.overloadReqMsg) {
                <div className='popup-button' onClick={this.handleInstrPerm}>Request Permission</div>
            }
            if (this.state.regFail || this.state.instrPermMsg || this.state.overloadReqMsg) {
                let popupContent = this.state.popupMessage.map((item) => {
                    return (
                        <li className="popup-item">{item}</li>
                    )
                })


                popup = (
                    <div className='popup-surrounder'>
                        <div className={this.state.popup ? 'popup' : 'popup-hidden'}>
                            <div className="popup-header">
                                <p>We weren't able to execute your request because of the following problems:</p>
                            </div>
                            <div className='popup-content'>
                                <ul>
                                    {popupContent}
                                </ul>
                            </div>
                            <div className='popup-button-holder'>
                                <div className='close-button' onClick={this.handlePopupClose}>Close</div>
                                {instrPermButton}
                                {overloadReqButton}
                            </div>
                        </div>
                    </div>
                )
            }


            if (this.state.resultsFound) {
                searchResult = this.state.searchResult.map((course) => {
                    console.log("mapping course result")
                    let registerButton = (<div></div>)
                    let open = (
                        course.enrollment_open && (course.enrollment_count < course.capacity)
                    )
                    console.log("instrPerm", course.instructor_permission_required)

                    if (open) {
                        registerButton = (
                            <div className="register-button"
                                open={open}
                                test={5}
                                sectionIndex={course.section_index}
                                onClick={this.handleCourseRegister} >
                                Register
                            </div >
                        )
                    }
                    return (
                        <div className='search-result-item'>
                            <div className='course-info'>
                                <div className='course-data'>
                                    <p>{course.course.name}</p>
                                    <p>{course.section_index}</p>
                                </div>
                                <div className='other-course-data'>
                                    <p>Instructor: {course.instructor.user_data.full_name}</p>
                                    <p>{course.timeslot.start_time}-{course.timeslot.end_time} {course.timeslot.days}</p>
                                </div>
                            </div>
                            <div className="course-enrollment">
                                <div className='enrollment-info'>
                                    <p>Enrollment: {course.enrollment_count} / {course.capacity}</p>
                                    <p>Prerequisites: {course.course.prereqs.join(', ')}</p>
                                </div>
                                <div className='register-holder'>
                                    <p>{open ? 'Open' : 'Closed'}</p>
                                    {registerButton}

                                </div>
                            </div>
                        </div>
                    )
                })

                searchResults = (
                    <div className='section' id='search-result-container'>
                        {searchResult}
                    </div>
                )
            }

        }
        else {
            loginForm = (
                <div id="login-container">
                    <p id="login-header">Login</p>
                    <form onSubmit={this.handleLoginSubmit}>
                        <label for="userId">User ID</label>
                        <input onChange={this.handleUsernameChange} type="text" value={this.state.user_id} name="userID" placeholder="user id" />
                        <label for="password">Password</label>
                        <input onChange={this.handlePasswordChange} type="text" value={this.state.password} name="password" placeholder="password" />
                        <button id='login-submit' type="submit">Submit</button>
                    </form>
                </div>
            )

        }


        return (
            < div id="global-wrapper" >
                { popup}
                <div id='content-wrapper'>
                    <div id="navbar">
                        <div className="navbar-item">
                            <p>The University</p>
                        </div>
                        <div className="navbar-item" id="navbar-button-holder">
                            {logoutButton}
                        </div>
                    </div>
                    <div>
                        {userData}
                        {currentCourses}
                        {restrictions}
                        {loginForm}
                    </div>
                    <div>
                        {search}
                    </div>
                    <div>
                        {searchResults}
                    </div>
                </div>
            </div >
        )

    }
}

// function App() {

//     const [message, setMessage] = useState(0);

//     useEffect(() => {
// fetch('/api').then(res => res.json()).then(data => {
//     setMessage(data.message);
// });
//     }, []);

//     return (
//         <div className="App">
//             <p>{message}</p>
//         </div>
//     );
// }

export default App;
