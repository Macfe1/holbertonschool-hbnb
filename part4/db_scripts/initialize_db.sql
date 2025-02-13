
-- User Table 
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY, -- (UUID format).
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Place Table 
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,  -- UUID format
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
    );

-- Review Table 
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,  -- UUID format
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT unique_user_place UNIQUE (user_id, place_id)
);

-- Amenity Table 
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,  -- UUID format
    name VARCHAR(255) UNIQUE
);

-- Place-Amenity relationship table
CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2a$12$Es7J5EmR2hq3rVdvDYc1se2GRYN1zsdCFzPe34/LBtpcoTuqnergO',True);

INSERT INTO Amenity (id, name) VALUES
('1d8ebc42-70b0-4b97-b6a8-a78f6bed43ce', 'WiFi'),
('bebc4542-4335-47f3-8757-352fc34017a6', 'Swimming Pool'),
('0abb30e3-5041-4576-aabe-0b9fad8e41d1', 'Air Conditioning');