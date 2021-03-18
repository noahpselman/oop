-- UNIVERSITY AFFILIATED PERSON
\COPY users(name, email, user_type) FROM 'users.csv' DELIMITER ',';

-- DEPARTMENTS
\COPY department(department_name, chair) FROM 'departments.csv' DELIMITER ',';

-- QUARTER
\COPY quarter(name, start_date, end_date) FROM 'quarter.csv' DELIMITER ',';

-- TIMESLOT
\COPY timeslot(days, starttime, endtime) FROM 'timeslot.csv' DELIMITER ',';

-- RESTRICTIONS
\COPY restriction(restriction) FROM 'restrictions.csv' DELIMITER ',';

-- STUDENT
\COPY student(university_id, expected_graduation, major, fulltime, maximum_enrollment) FROM 'students.csv' DELIMITER ',';

-- STUDENT RESTRICTIONS
\COPY student_restrictions(university_id, restriction) FROM 'student_restriction.csv' DELIMITER ',';

-- INTRUCTORS
\COPY instructor(university_id, department) FROM 'instructor.csv' DELIMITER ',';

-- COURSE
\COPY course(name, course_id, department, is_lab, lab_id) FROM 'courses.csv' DELIMITER ',' NULL 'NULL';

-- COURSE SECTION
\COPY course_section(section_number, course_id, department, quarter, timeslot, enrollment_open, state, instructor_id, capacity, instructor_permission_required) FROM 'course_sections.csv' DELIMITER ',';

-- ENROLLMENT
\COPY enrollment(section_number, course_id, department, quarter, student_id, type, grade, state) FROM 'enrollment.csv' DELIMITER ',';

-- PREREQS
\COPY prereqs(course_id, course_department, prereq_id, prereq_department) FROM 'prereqs.csv' DELIMITER ',';