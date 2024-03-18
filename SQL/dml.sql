-- Populate Authors Table
INSERT INTO Authors (first_name, last_name, bio)
VALUES 
('J.K.', 'Rowling', 'Author of the Harry Potter series'),
('George', 'Orwell', 'Author of 1984 and Animal Farm'),
('Jane', 'Austen', 'Author of Pride and Prejudice'),
('Mark', 'Twain', 'Author of Adventures of Huckleberry Finn'),
('F. Scott', 'Fitzgerald', 'Author of The Great Gatsby'),
('Agatha', 'Christie', 'Mystery writer known for Hercule Poirot'),
('Ernest', 'Hemingway', 'Author of The Old Man and the Sea'),
('Isaac', 'Asimov', 'Science fiction author known for Foundation series');

-- Populate Publishers Table
INSERT INTO Publishers (publisher_name, address)
VALUES 
('Bloomsbury', '50 Bedford Square, London'),
('Penguin Books', '80 Strand, London'),
('HarperCollins', '195 Broadway, New York City'),
('Random House', '1745 Broadway, New York City'),
('Simon & Schuster', '1230 Avenue of the Americas, New York City'),
('Macmillan', '120 Broadway, New York City'),
('Hachette', '1290 Avenue of the Americas, New York City'),
('Wiley', '111 River Street, Hoboken');

-- Populate Books Table
INSERT INTO Books (title, author_id, publisher_id, published_date, isbn, available_copies)
VALUES 
('Harry Potter and the Philosopher''s Stone', 1, 1, '1997-06-26', '9780747532699', 10),
('1984', 2, 2, '1949-06-08', '9780451524935', 7),
('Pride and Prejudice', 3, 3, '1813-01-28', '9780141040349', 5),
('Adventures of Huckleberry Finn', 4, 4, '1884-12-10', '9780486280615', 8),
('The Great Gatsby', 5, 5, '1925-04-10', '9780743273565', 6),
('Murder on the Orient Express', 6, 6, '1934-01-01', '9780007119318', 9),
('The Old Man and the Sea', 7, 7, '1952-09-01', '9780684801223', 5),
('Foundation', 8, 8, '1951-06-01', '9780553293357', 7),
('Harry Potter and the Half Blood Prince', 1, 1, '1997-06-26', '978074753', 10),
('Terrible Book', 1, 1, '1997-06-26', '4753', 10);

-- Populate Members Table
INSERT INTO Members (first_name, last_name, email, phone, join_date)
VALUES 
('Alice', 'Smith', 'alice.smith@email.com', '123-456-7890', '2023-08-25'),
('Bob', 'Johnson', 'bob.johnson@email.com', '234-567-8901', '2023-09-01'),
('Charlie', 'Williams', 'charlie.williams@email.com', '345-678-9012', '2023-08-20'),
('David', 'Brown', 'david.brown@email.com', '456-789-0123', '2023-09-10'),
('Eva', 'Jones', 'eva.jones@email.com', '567-890-1234', '2023-08-30'),
('Frank', 'Davis', 'frank.davis@email.com', '678-901-2345', '2023-09-05'),
('Grace', 'Miller', 'grace.miller@email.com', '789-012-3456', '2023-08-28'),
('Hugo', 'Garcia', 'hugo.garcia@email.com', '890-123-4567', '2023-09-12'),
('Ross', 'Geller', 'ross.geller@email.com', '890-123-4567', '2022-01-01'),
('Rachel', 'Green', 'rachel.green@email.com', '890-123-4567', '2022-01-01'),
('Monica', 'Geller', 'monica.geller@email.com', '890-123-4567', '2022-01-01');


-- Populate Borrowing Table
-- Assuming members borrow books in the same order they are listed
INSERT INTO Borrowing (book_id, member_id, borrow_date, return_date)
VALUES 
(1, 1, '2023-09-01', NULL),
(2, 2, '2023-09-05', '2023-09-20'),
(3, 3, '2023-08-25', '2023-09-10'),
(4, 4, '2023-09-10', NULL),
(5, 5, '2023-09-15', NULL),
(6, 6, '2023-09-07', '2023-09-21'),
(7, 7, '2023-08-30', '2023-09-15'),
(8, 8, '2023-09-12', NULL),
(9, 10, '2023-09-12', NULL),
(9, 11, '2023-09-12', NULL),
(1, 9, '2023-09-12', NULL);
