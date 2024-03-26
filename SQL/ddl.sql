DROP DATABASE IF EXISTS HealthAndFitnessClubManagementSystem;
CREATE DATABASE HealthAndFitnessClubManagementSystem;

-- Members Table
CREATE TABLE Members (
    name VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    current_weight INTEGER NOT NULL,
    goal_weight INTEGER NOT NULL,
    goal_date DATE NOT NULL
);

-- Member Notifications Table
CREATE TABLE MemberNotifications (
    member_name VARCHAR(255) REFERENCES Members(name),
    notification_text TEXT NOT NULL
);

-- Trainers Table
CREATE TABLE Trainers (
    name VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- Trainer Notifications Table
CREATE TABLE TrainerNotifications (
    trainer_name VARCHAR(255) REFERENCES Trainers(name),
    notification_text TEXT NOT NULL
);

CREATE TABLE Sessions (
    session_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) REFERENCES Members(name),
    trainer_name VARCHAR(255) REFERENCES Trainers(name),
    date_and_time TIMESTAMP NOT NULL
);

CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY


);

CREATE TABLE Participants (

);