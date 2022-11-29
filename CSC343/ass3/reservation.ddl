/* Since we used BCNF to decomposite relations, there is no redundancy, 
and the NULL value is not allowed in any attribute and none of them 
have a default value. 

All the constraints from the problem descrption are enforced without 
using triggers or assertions. 

However, based on the real-world knowledge of reservations, one skipper 
cannot reserve two crafts at the same time, and one craft cannot be 
reserved by two skippers at the same time. Therefore, we thought to add two new 
FDs: (sID, day -> cID) and (cID, day -> sID), to avoid double-booking. In the 
code, these two FDs would be represented by UNIQUE(sID, day) and UNIQUE(cID, day)
in the reserve relation. However, since there is only a day attribute that represents 
the starting time of the reservation, we cannot know when the craft will be returned. 
Therefore, with the current schema and FDs, we cannot totally avoid double-bookings, and 
the above two new FDs only avoids the same craft being reserved with the same 
starting time, and the same skipper reverses two crafts with the same starting 
time. As a result, we did not add these two new FDs, and we conclude that with the given FDs 
and attributes, and without using assertions or triggers, we cannot enforce this contraint to
totally avoid double-bookings.*/

drop schema if exists reservation cascade;
create schema reservation;
set search_path to reservation;

CREATE TABLE skipper (
    -- Identifies the skipper
    sID INT PRIMARY KEY,

    -- The skipper's name
    sName TEXT NOT NULL,
    
    -- The skipper's skill (a number between 0 and 5, inclusive)
    -- Decimal number should be allowed
    rating DECIMAL NOT NULL
        CHECK (0 <= rating AND rating <= 5),
    
    -- The skipper's age (a number greater than 0)
    -- Only integer is allowed, as a person cannot be 22.2 years old
    age INT NOT NULL
        CHECK (age > 0)
);

CREATE TABLE craft (
    -- Identifies the craft
    cID INT PRIMARY KEY,

    -- The craft's name
    cName TEXT NOT NULL,
    
    -- The craft's length, in feet
    -- Decimal number should be allowed
    -- The craft should have a length greater than 0
    length DECIMAL NOT NULL
    	CHECK (length > 0)
);

CREATE TABLE reserve (
    -- Identifies the skipper
    -- After adding "REFERENCES", the sID attribute cannot be NULL, as tested on psql
    sID INT REFERENCES skipper,

    -- Identifies the craft
    -- After adding "REFERENCES", the cID attribute cannot be NULL, as tested on psql
    cID INT REFERENCES craft,
    
    -- The date and time the craft is reserved (starting time)
    day timestamp NOT NULL,
    
    -- Prevent Double-Booking
    /* UNIQUE(sID, day),
    UNIQUE(cID, day) */
);