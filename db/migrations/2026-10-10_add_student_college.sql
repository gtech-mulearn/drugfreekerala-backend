-- Adds the "Are you a student?" answer and the student's college to pledges.
-- Run BEFORE deploying the code that uses these columns: the new model writes
-- them on every insert, so pledges fail until they exist. All columns are
-- nullable, so the code that is live today keeps working after this runs.
ALTER TABLE user_data
    ADD COLUMN is_student BOOLEAN NULL AFTER email,
    ADD COLUMN college_id VARCHAR(36) NULL AFTER is_student,
    ADD COLUMN college_name VARCHAR(255) NULL AFTER college_id;
