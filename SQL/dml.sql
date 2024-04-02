INSERT INTO Admins (admin_name, password)
VALUES
('Admin', 'IAMADMIN');

INSERT INTO Trainers (trainer_name, password, start_time, end_time)
VALUES
('Jackson', 'password', '5:00:00', '15:00:00');

INSERT INTO Members (member_name, password, current_weight, goal_weight, goal_date)
VALUES
('Jackson', 'password', '250', '200', '2003-10-24'),
('Eve', 'password', '200', '200', '2003-10-24');

INSERT INTO Sessions (member_name, trainer_name, start_date_and_time, end_date_and_time)
VALUES
('Jackson', 'Jackson', '2000-10-23 7:00:00', '2000-10-23 9:00:00');

INSERT INTO Rooms (room_description)
VALUES
('Bike Room'),
('Weights Room'),
('Cardio Room'),
('Sauna');

INSERT INTO Classes (class_name, start_date_and_time, end_date_and_time, room_id)
VALUES
('Jackson class', '2000-10-23 7:00:00', '2000-10-23 9:00:00', '2'),
('Another class', '2000-10-23 7:00:00', '2000-10-23 9:00:00', '1');

INSERT INTO Participants (class_id, member_name)
VALUES
('1', 'Jackson'),
('2', 'Jackson'),
('1', 'Eve');