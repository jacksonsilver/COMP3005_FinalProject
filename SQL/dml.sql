INSERT INTO Admins (admin_name, password)
VALUES
('ADMIN', 'IAMADMIN');

INSERT INTO Members (member_name, password, current_weight, goal_weight, goal_date)
VALUES
('Eve', 'IAmEve', '200', '190', '2024-04-29'),
('Davis', 'IAmDavis', '200', '190', '2024-04-27'),
('Alison', 'IAmAlison', '180', '190', '2024-06-20'),
('Marianna', 'IAmMarianna', '140', '130', '2024-09-20');

INSERT INTO Trainers (trainer_name, password, start_time, end_time)
VALUES
('John', 'IAmJohn', '5:00:00', '15:00:00'),
('Dimitra', 'IAmDi', '6:00:00', '18:00:00'),
('Mark', 'IAmMark', '7:00:00', '16:00:00');

INSERT INTO Sessions (member_name, trainer_name, start_date_and_time, end_date_and_time)
VALUES
('Eve', 'John', '2024-04-23 7:00:00', '2024-04-23 9:00:00'),
('Eve', 'John', '2024-04-25 10:00:00', '2024-04-25 11:00:00'),
('Eve', 'Dimitra', '2024-04-26 14:00:00', '2024-04-26 15:00:00'),
('Davis', 'Dimitra', '2024-04-23 7:00:00', '2024-04-23 9:00:00'),
('Alison', 'Mark', '2024-04-23 7:00:00', '2024-04-23 9:00:00'),
('Marianna', 'John', '2024-04-23 10:00:00', '2024-04-23 11:00:00');

INSERT INTO Rooms (room_description)
VALUES
('Bike Room'),
('Weights Room'),
('Cardio Room'),
('Sauna');

INSERT INTO Classes (class_name, start_date_and_time, end_date_and_time, room_id)
VALUES
('Kickin Cardio Class', '2000-10-23 7:00:00', '2000-10-23 9:00:00', '3'),
('Heat Wave Class', '2000-10-23 7:00:00', '2000-10-23 9:00:00', '4');

INSERT INTO Participants (class_id, member_name)
VALUES
('1', 'Marianna'),
('1', 'Eve'),
('2', 'Eve'),
('2', 'Alison');