DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS quarter CASCADE;
DROP TABLE IF EXISTS restriction CASCADE;
DROP TABLE IF EXISTS timeslot CASCADE;
DROP TABLE IF EXISTS course CASCADE;
DROP TABLE IF EXISTS course_section CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS student_restrictions CASCADE;
DROP TABLE IF EXISTS instructor CASCADE;
DROP TABLE IF EXISTS prereqs CASCADE;
DROP TABLE IF EXISTS enrollment CASCADE;
DROP TABLE IF EXISTS auditor CASCADE;
DROP TABLE IF EXISTS registration CASCADE;

DROP TYPE IF EXISTS user_type;
DROP TYPE IF EXISTS course_section_state;
DROP TYPE IF EXISTS enrollment_type;
DROP TYPE IF EXISTS enrollment_state;
DROP TYPE IF EXISTS grade;
DROP TYPE IF EXISTS registration_status;

CREATE TYPE user_type AS ENUM ('Student', 'Instructor');

CREATE TABLE users (
    university_id serial,
    name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    user_type user_type,
    PRIMARY KEY (university_id)
);

CREATE TABLE department (
    department_name varchar(4),
    chair int,
    PRIMARY KEY (department_name),
    FOREIGN KEY (chair) REFERENCES users (university_id)
);

CREATE TABLE quarter (
    name varchar(11),
    start_date date,
    end_date date,
    PRIMARY KEY (name)
);

CREATE TABLE restriction (
    restriction varchar(30),
    PRIMARY KEY (restriction)
);

CREATE TABLE timeslot (
    id serial,
    days varchar(2) NOT NULL,
    starttime time NOT NULL,
    endtime time NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE student (
    university_id int,
    expected_graduation varchar(11) NOT NULL,
    major varchar(4) NOT NULL,
    fulltime boolean NOT NULL DEFAULT TRUE,
    maximum_enrollment int DEFAULT 3,
    PRIMARY KEY (university_id),
    FOREIGN KEY (university_id) REFERENCES users,
    FOREIGN KEY (expected_graduation) REFERENCES quarter (name),
    FOREIGN KEY (major) REFERENCES department (department_name)
);

CREATE TABLE student_restrictions (
    university_id int,
    restriction varchar(30),
    PRIMARY KEY (university_id, restriction),
    FOREIGN KEY (restriction) REFERENCES restriction
);

CREATE TABLE instructor (
    university_id int,
    department varchar(4),
    PRIMARY KEY (university_id),
    FOREIGN KEY (university_id) REFERENCES users,
    FOREIGN KEY (department) REFERENCES department (department_name)
);

CREATE TABLE course (
    course_id int,
    department varchar(4),
    name varchar(120),
    is_lab boolean,
    lab_id int,
    PRIMARY KEY (course_id, department),
    FOREIGN KEY (department) REFERENCES department (department_name)
);


CREATE TYPE course_section_state AS ENUM ('PRESTART', 'ONGOING', 'FINISHED');

CREATE TABLE course_section (
    section_number int,
    department varchar(4),
    course_id int,
    quarter varchar(11),
    timeslot int,
    enrollment_open boolean,
    state course_section_state,
    instructor_id int,
    capacity int,
    instructor_permission_required boolean,
    PRIMARY KEY (section_number, course_id, department, quarter),
    FOREIGN KEY (course_id, department) REFERENCES course (course_id, department),
    FOREIGN KEY (quarter) REFERENCES quarter (name),
    FOREIGN KEY (timeslot) REFERENCES timeslot (id),
    FOREIGN KEY (instructor_id) REFERENCES instructor (university_id)
);

CREATE TABLE prereqs (
    course_id int,
    course_department varchar(4),
    prereq_id int,
    prereq_department varchar(4),
    PRIMARY KEY (course_id, course_department, prereq_id, prereq_department),
    FOREIGN KEY (course_id, course_department) REFERENCES course (course_id, department),
    FOREIGN KEY (prereq_id, prereq_department) REFERENCES course (course_id, department)
);


CREATE TYPE enrollment_type AS ENUM ('REGULAR', 'PASS/FAIL');
CREATE TYPE enrollment_state AS ENUM ('COMPLETE', 'TENTATIVE', 'PENDING');
CREATE TYPE grade AS ENUM ('A', 'B', 'C', 'D', 'F', 'P');

CREATE TABLE enrollment (
    section_number int,
    course_id int,
    department varchar(4),
    quarter varchar(11),
    student_id int,
    type enrollment_type,
    grade grade,
    state enrollment_state,
    PRIMARY KEY (section_number, course_id, department, quarter, student_id),
    FOREIGN KEY (section_number, course_id, department, quarter)
        REFERENCES course_section (section_number, course_id, department, quarter),
    FOREIGN KEY (student_id) REFERENCES student (university_id)
);

CREATE TABLE auditor (
    section_number int,
    course_id int,
    department varchar(4),
    quarter varchar(11),
    student_id int,
    PRIMARY KEY (section_number, course_id, department, quarter, student_id),
    FOREIGN KEY (section_number, course_id, department, quarter)
        REFERENCES course_section (section_number, course_id, department, quarter),
    FOREIGN KEY (student_id) REFERENCES student (university_id)
);

CREATE TYPE registration_status AS ENUM ('ENROLLED', 'PENDING', 'TENTATIVE');

CREATE TABLE registration (
    section_number int,
    course_id int,
    department varchar(4),
    quarter varchar(11),
    student_id int,
    status registration_status,
    PRIMARY KEY (section_number, course_id, department, quarter, student_id),
    FOREIGN KEY (section_number, course_id, department, quarter)
        REFERENCES course_section (section_number, course_id, department, quarter),
    FOREIGN KEY (student_id) REFERENCES student (university_id)
);






-- -- TODO: quarter, restrictions, student_course link

