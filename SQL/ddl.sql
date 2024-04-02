--DROP DATABASE IF EXISTS HealthAndFitnessClubManagementSystem;
--CREATE DATABASE HealthAndFitnessClubManagementSystem;

CREATE TABLE Admins (
    admin_name VARCHAR(255) PRIMARY KEY,
    password VARCHAR (255) NOT NULL
);

CREATE TABLE Members (
    member_name VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    current_weight INTEGER NOT NULL,
    goal_weight INTEGER NOT NULL,
    goal_date DATE NOT NULL
);

CREATE TABLE Trainers (
    trainer_name VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE MemberNotifications (
    member_name VARCHAR(255) REFERENCES Members(member_name),
    notification_text TEXT NOT NULL
);

CREATE TABLE TrainerNotifications (
    trainer_name VARCHAR(255) REFERENCES Trainers(trainer_name),
    notification_text TEXT NOT NULL
);

CREATE TABLE Routines (
    routine_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) REFERENCES Members(member_name),
    routine_text TEXT NOT NULL
);

CREATE TABLE Achievements (
    member_name VARCHAR(255) REFERENCES Members(member_name),
    achievement_text TEXT NOT NULL
);

CREATE TABLE Billings (
    billing_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) REFERENCES Members(member_name),
    billing_text TEXT NOT NULL,
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE Reports (
    report_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) REFERENCES Members(member_name),
    report_text TEXT NOT NULL
);

CREATE TABLE Sessions (
    session_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) REFERENCES Members(member_name),
    trainer_name VARCHAR(255) REFERENCES Trainers(trainer_name),
    start_date_and_time TIMESTAMP NOT NULL,
    end_date_and_time TIMESTAMP NOT NULL
);

CREATE TABLE Rooms (
    room_id SERIAL PRIMARY KEY,
    room_description TEXT NOT NULL
);

CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    start_date_and_time TIMESTAMP NOT NULL,
    end_date_and_time TIMESTAMP NOT NULL,
    room_id INTEGER REFERENCES Rooms(room_id)
);

CREATE TABLE Participants (
    class_id INTEGER REFERENCES Classes(class_id),
    member_name VARCHAR(255) REFERENCES Members(member_name)
);

-- Function that provides trainer notifications and then deletes them
CREATE OR REPLACE FUNCTION select_and_delete_trainernotifications(trainer_name_param VARCHAR)
RETURNS TABLE (deleted_trainer_name VARCHAR(255), notification_text TEXT) AS $$
BEGIN
    RETURN QUERY
    DELETE FROM TrainerNotifications
    WHERE trainer_name = trainer_name_param
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION select_and_delete_membernotifications(member_name_param VARCHAR)
RETURNS TABLE (deleted_member_name VARCHAR(255), notification_text TEXT) AS $$
BEGIN
    RETURN QUERY
    DELETE FROM MemberNotifications
    WHERE member_name = member_name_param
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Function that notifies members when one of their reports is resolved
CREATE OR REPLACE FUNCTION notify_member_on_report_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO MemberNotifications (member_name, notification_text)
    VALUES (OLD.member_name, 'A report with ID ' || OLD.report_id || ' was deleted. Report description: ' || OLD.report_text);

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger that ensures deleted reports notify the member who creates them
CREATE TRIGGER report_delete_trigger
AFTER DELETE ON Reports
FOR EACH ROW
EXECUTE FUNCTION notify_member_on_report_delete();

-- Function that adds a member notification when an achievement is added
CREATE OR REPLACE FUNCTION notify_member_on_achievement_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO MemberNotifications (member_name, notification_text)
    VALUES (NEW.member_name, 'An achievement was added: ' || NEW.achievement_text);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger that adds notification to member anytime member gets an achievement
CREATE TRIGGER achievement_insert_trigger
AFTER INSERT ON Achievements
FOR EACH ROW
EXECUTE FUNCTION notify_member_on_achievement_insert();

-- Function to send notifications to members and trainers of new session
CREATE OR REPLACE FUNCTION notify_member_and_trainer_of_new_session()
RETURNS TRIGGER AS $$
BEGIN
    -- Notify the member
    INSERT INTO MemberNotifications(member_name, notification_text)
    VALUES (NEW.member_name, 'A session with Trainer ' || NEW.trainer_name || ' has been scheduled from ' || TO_CHAR(NEW.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(NEW.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS'));

    -- Notify the trainer
    INSERT INTO TrainerNotifications(trainer_name, notification_text)
    VALUES (NEW.trainer_name, 'A session with Member ' || NEW.member_name || ' has been scheduled from ' || TO_CHAR(NEW.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(NEW.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS'));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger that notifies members and trainers (appropriate) of new sessions that they are in
CREATE TRIGGER session_notification_trigger
AFTER INSERT ON Sessions
FOR EACH ROW
EXECUTE FUNCTION notify_member_and_trainer_of_new_session();

-- Function that notifies members and trainers of their session that was deleted
CREATE OR REPLACE FUNCTION notify_deleted_session()
RETURNS TRIGGER AS
$$
BEGIN
    -- Notify Member
    INSERT INTO MemberNotifications (member_name, notification_text)
    VALUES (OLD.member_name, 'The session with Trainer ' || OLD.trainer_name || ' from ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' has been cancelled.');

    -- Notify Trainer
    INSERT INTO TrainerNotifications (trainer_name, notification_text)
    VALUES (OLD.trainer_name, 'The session with Member ' || OLD.member_name || ' from ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' has been cancelled.');

    RETURN OLD;
END;
$$
LANGUAGE plpgsql;

-- Trigger that notifies members and trainers of deleted sessions they are in
CREATE TRIGGER session_deleted_trigger
AFTER DELETE ON Sessions
FOR EACH ROW
EXECUTE FUNCTION notify_deleted_session();

-- Function that notifies members and trainers where their session is updated
CREATE OR REPLACE FUNCTION notify_updated_session()
RETURNS TRIGGER AS
$$
BEGIN
    -- Notify Member
    INSERT INTO MemberNotifications (member_name, notification_text)
    VALUES (NEW.member_name, 
            'The session with Trainer ' || NEW.trainer_name || ' has been updated from ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ', to ' || TO_CHAR(NEW.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(NEW.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS'));

    -- Notify Trainer
    INSERT INTO TrainerNotifications (trainer_name, notification_text)
    VALUES (NEW.trainer_name, 
            'The session with Member ' || NEW.member_name || ' has been updated from ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ', to ' || TO_CHAR(NEW.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(NEW.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS'));

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Trigger that notifies members and trainers when their session is updated (the date)
CREATE TRIGGER session_updated_trigger
AFTER UPDATE ON Sessions
FOR EACH ROW
EXECUTE FUNCTION notify_updated_session();

-- Function that adds a billing describing a member getting refunded for a cancelled session.
CREATE OR REPLACE FUNCTION add_refund_billing()
RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO Billings (member_name, billing_text)
    VALUES (OLD.member_name,
            'Refund for cancelled session (id = ' || OLD.session_id || ') with Trainer' || OLD.trainer_name || ' on ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') ||
            '. Refund amount: $50 ');

    RETURN OLD;
END;
$$
LANGUAGE plpgsql;

-- Trigger that adds billling about cancelled session when a session is cancelled (deleted)
CREATE TRIGGER session_deleted_billing_trigger
AFTER DELETE ON Sessions
FOR EACH ROW
EXECUTE FUNCTION add_refund_billing();

-- Function that adds a member notification about a class they have registered for.
CREATE OR REPLACE FUNCTION notify_member_on_class_participation()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO MemberNotifications (member_name, notification_text)
    SELECT NEW.member_name, 'You have registered for the class ' || c.class_id || ' - ' || c.class_name || ' from ' ||
    TO_CHAR(c.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ' to ' || TO_CHAR(c.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
    ' in room ' || c.room_id || '.'
    FROM Classes c
    WHERE c.class_id = NEW.class_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger that makes member notification everytime members register for class.
CREATE TRIGGER participant_added_to_class_trigger
AFTER INSERT ON Participants
FOR EACH ROW
EXECUTE FUNCTION notify_member_on_class_participation();

-- Function to notify members of deleted classes and add billing for refunding
CREATE OR REPLACE FUNCTION notify_members_on_class_deletion(class_id_to_delete INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Notify each participant of the deleted class
    INSERT INTO MemberNotifications (member_name, notification_text)
    SELECT p.member_name,
           'The class ' || c.class_id || ' - ' || c.class_name || ' that you were registered for has been cancelled.'
    FROM Participants p
    INNER JOIN Classes c ON p.class_id = c.class_id
    WHERE c.class_id = class_id_to_delete;

    -- Add billing for refunding
    INSERT INTO Billings (member_name, billing_text, processed)
    SELECT p.member_name,
           'Refund $25 for cancelled class ' || c.class_id || ' - ' || c.class_name || ')',
           FALSE
    FROM Participants p
    INNER JOIN Classes c ON p.class_id = c.class_id
    WHERE c.class_id = class_id_to_delete;

    -- Delete Participants for the deleted class
    DELETE FROM Participants
    WHERE class_id = class_id_to_delete;

    -- Delete Class
    DELETE FROM Classes
    WHERE class_id = class_id_to_delete;

    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Function to notify members of updated class start/end time
CREATE OR REPLACE FUNCTION notify_members_on_class_time_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Notify each participant of the updated class start/end time
    INSERT INTO MemberNotifications (member_name, notification_text)
    SELECT p.member_name,
           'The time of the class ' || c.class_id || ' - ' || c.class_name || ' has been updated from ' || TO_CHAR(OLD.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(OLD.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || ', to ' || TO_CHAR(NEW.start_date_and_time, 'YYYY-MM-DD HH24:MI:SS') || 
            ' to ' || TO_CHAR(NEW.end_date_and_time, 'YYYY-MM-DD HH24:MI:SS')
    FROM Participants p
    INNER JOIN Classes c ON p.class_id = c.class_id
    WHERE c.class_id = NEW.class_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger to notify members of updated class start/end time
CREATE TRIGGER class_time_updated_trigger
AFTER UPDATE OF start_date_and_time, end_date_and_time ON Classes
FOR EACH ROW
EXECUTE FUNCTION notify_members_on_class_time_update();

-- Function to notify members of updated class room
CREATE OR REPLACE FUNCTION notify_members_on_class_room_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Notify each participant of the updated class room
    INSERT INTO MemberNotifications (member_name, notification_text)
    SELECT p.member_name,
           'The room for the class ' || c.class_id || ' - ' || c.class_name || ' has been updated from ' ||
           OLD.room_id || ' to ' || NEW.room_id
    FROM Participants p
    INNER JOIN Classes c ON p.class_id = c.class_id
    WHERE c.class_id = NEW.class_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger to notify members of updated class room
CREATE TRIGGER class_room_updated_trigger
AFTER UPDATE OF room_id ON Classes
FOR EACH ROW
EXECUTE FUNCTION notify_members_on_class_room_update();