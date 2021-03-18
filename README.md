# Noah's OOP/Web Dev Final Project



### Set up postgres db
I followed the instructions in the [postgres section here](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-database) to install postgres on my WSL (Ubuntu 20.04).  If you already have postgres installed, skip to step 3 to create the db relevant to this project.

1. `sudo apt update`
2. `sudo apt install postgresql postgresql-contrib`
3. Once you're sure that worked, create a database.  Since I used harry potter themed fake data we can call our database hogwarts.  Start up psql using `sudo -u postgres psql` and enter `CREATE DATABASE hogwarts`
4. If all that worked we can upload the fake data.  cd into oop-proj/src and run `sudo -u postgres psql hogwarts -f create_tables.sql` (from your regular terminal, not psql)
5. Then, to upload the data cd into oop-proj/fake-data and run `sudo -u postgres psql hogwarts -f upload_data.sql`
6. Hopefully all this worked.  Now, you'll have to put your credentials in a .py file, because that's how I decided to do it.  In oop-proj/src, create db_conf.py.  Inside create the following function with your credentials:
```
def db_conf():
    return {
        'dbname': 'hogwarts',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }
```
I am praying that this is sufficient for my program to find your database.

### Set up Mongo db
Mongo is used in a very limited sense in this application. The application simply logs when any flask endpoint is hit.
I create a free cloud-based database following by following the procedure to start a free account on [this website](https://www.mongodb.com/3).  If you don't want to do that you can you my credentials, I don't care.  Create a function in oop-proj/src/db_conf.py either using or replacing my information
```
def mongo_conf():
    return "mongodb+srv://oop-proj:best-proj-ever99@cluster0.bez9g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
```
Warning: at times the logging slows down the program, if that's an issue, please try commenting out the logging commands in oop-proj/src/api/api.py then re-running `flask run`

### Starting up the project
0. Start the postgres database by entering `sudo service postgresql start`
1. Download the python packages in requirements.txt (requires python3 and some virtual environment to be installed)
2. Download the javascript dependencies using npm install (requires npm to be installed)
3. In a terminal activate flask with `run flask`
4. In another terminal start the javascript with `npm start` (or yarn start if you're doing that instead)

### Video demonstration of project features
A video demo of some of the features can be found at here: YOUTUBE LINK

### Running Tests
A note about my experience attempting test driven development:
I found that writing tests prior to implementing features slowed me down substantially.  Originally I wrote tests for each type of attribute on each object.  However, the interfaces, methods, and existence of my objects evolved so dramatically that there were sets of tests I had spent hours on for objects that disappeared.  I then adopted the strategy writing tests  after I had built a basic structure for a bounded context.  This still slowed me down so I began only testing the public interface of classes.  With more time I would expand this to be more comprehensive.  However, these tests will notify me if any change I make breaks the major parts of my code.

To run the tests simply execute the command pytest in the terminal while in oop-proj/src
Currently tests are written for the following class:
- SQL DB
- DatabaseHelper

### Features
My application represents a prototype of a university course registration system with the following capabilities:
- Students can search courses by department, instructor name, and course number.  Doing so will mock an email send.
- Students can register for courses they've searched by clicking a "register" button.  Doing so will mock an email send.
- Courses students have registered for appear on their home page for a particular quarter
- Students can drop courses they've registered for by clicking a drop button
- Some courses require instructor permission, students will be given an opportunity to request permission for these when attempting to register
- Students will be given an option request an overload if they want to register for more courses than their capacity
- Some courses have labs, students will be given a list of labs to choose from when attempting to enroll in a course with a lab
- When a student attempts to register for a section with time conflict with another course, they're shown a list of alternative sections.
- Students can see their restriction
- The system will check numberous criteria to determine of a student is eligble to register for a course:  whether they have restrictions, if they have met the prereqs, if there are time conflicts with other courses, if the course requires special permission, if the course is full, etc.  (This is done in a pretty nifty way using the strategy pattern).


### Design Notes
- All the important data are stored in a sql db.  Two entity class are instantiated for nearly every process in the application: Student and CourseSection.

#### Student
- Students mostly just hold data relevant to... that student
- Students hold a user object that knows data help by all types of users: name, university_id, email
- For a most operations students are mainly a data structure passed between controller
- Students are generally instantiated from a student id as one of the first steps after an endpoint gets hit
- Many attributes of students are required only for a single use case - these are setup to lazily load from the database only when these attributes are called

#### CourseSection
- Course sections are also mostly just used as data structures with information relevant to many procedures
- Course sections are identified by section_number, course_id, quarter, and department and are instantiated from these variables to execute processes contingent on various aspects of course section data

#### Registration
- The registration process involves a registrar first telling a validator to cycling through "Validations" - validations all respond to an "is_valid" method.  The validator returns a report with details about a students eligibility for a class.  The registrar passes that report to a RegistrationFailureManager which performs the corresponding actions.  Then the registrar adds an enrollment to the database (or tries to) and sends the ValidationReport to the frontend.

### Known Limitation (a jumping off point for graders)

- As of Wednesday, 3/17 my App.js is a heaping mess that follows no object-oriented principles.  While originally I hoped to do this, my esteemed Web Development professor advised my to just get everything working before I start refactoring in multiple files.  I understand that in react sharing a state between components living in different files can introduce some complexities that may have prevented me from delivering a functioning product.  I plan on refactoring the front end before my web development project is due on Sunday, 3/21
- Generally the backend is ahead of the front end meaning that I haven't created a working user interface for all the features that the backend supports.  For example, I haven't build support for displaying a students course history or for allowing a student to change labs.
- Tentative and Pending enrollments (created when students request overload or instructor permission) display on the front end as normal courses
- Currently students have an attribute called current courses - this a list of CourseSection objects because CourseSections have all the data that the front end might want to display.  In reality students should be holding Enrollments, objects that represent a students participation in a course and holds information particular to that relationship (ie if they're auditing or taking a course P/F and their grade).
- I allow students to register for labs without registering for the corresponding course, (even though the opposite is not allowed).
- 
