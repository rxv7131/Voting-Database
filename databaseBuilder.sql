DROP DATABASE IF EXISTS americanDreamElect;
CREATE DATABASE americanDreamElect;
USE americanDreamElect;

CREATE TABLE Candidate(
    candidateID INT NOT NULL AUTO_INCREMENT,
    fName VARCHAR(20),
    midInitial CHAR(1),
    lName VARCHAR(20),
    picture VARCHAR(50),
    position VARCHAR(30),
    proBackground VARCHAR(200),
    bio VARCHAR(8000),
    PRIMARY KEY (candidateID)
);

CREATE TABLE Ballot(
    ballotID INT NOT NULL AUTO_INCREMENT,
    dateCast DATETIME,
    PRIMARY KEY(ballotID)
);

CREATE TABLE Voters(
    voterID INT NOT NULL AUTO_INCREMENT,
    societyID INT,
    fName VARCHAR(20),
    lName VARCHAR(20),
    email VARCHAR(80),
    credential1 VARCHAR(30),
    credential2 INT,
    canVote BOOLEAN, 
    PRIMARY KEY (voterID)
);

CREATE TABLE Admins(
    adminID INT NOT NULL AUTO_INCREMENT,
    societyID INT,
    fName VARCHAR(20),
    lName VARCHAR(20),
    email VARCHAR(80),
    credential1 VARCHAR(30),
    credential2 INT,
    PRIMARY KEY (adminID)
);

CREATE TABLE Society(
    societyID INT NOT NULL AUTO_INCREMENT,
    societyName VARCHAR(50),
    logo VARCHAR(50),
    PRIMARY KEY (societyID)
); 

CREATE TABLE Election(
    electionID INT NOT NULL AUTO_INCREMENT,
    societyID INT, 
    electionTitle VARCHAR(100),
    startDate DATE,
    endDate DATE,
    information VARCHAR(800),
    PRIMARY KEY (electionID)
);

CREATE TABLE Roles(
    roleID INT NOT NULL AUTO_INCREMENT,
    electionID INT,
    roleTitle VARCHAR(50) NOT NULL,
    roleDescription VARCHAR(8000),
    votingType INT,
    PRIMARY KEY (roleID, roleTitle)
);

CREATE TABLE CandidateRole(
    selectionID INT NOT NULL AUTO_INCREMENT,
    roleTitle VARCHAR(50) NOT NULL,
    candidateID INT,
    roleId INT,
    candStatement VARCHAR(8000),
    PRIMARY KEY (selectionID)
);

CREATE TABLE BallotVote(
    ballotID INT NOT NULL,
    fieldTitle VARCHAR(50),
    candidateID INT,
    optionID INT
);

CREATE TABLE Initiative(
    initiativeID INT NOT NULL AUTO_INCREMENT,
    electionID INT,
    initiativeTitle VARCHAR(50) NOT NULL,
    descriptionFielD VARCHAR(8000),
    votingType INT,
    PRIMARY KEY (initiativeID, initiativeTitle)
);

CREATE TABLE OptionInitiative(
    selectionID INT NOT NULL AUTO_INCREMENT,
    initiativeTitle VARCHAR(50) NOT NULL,
    initiativeID INT,
    optionID INT,
    PRIMARY KEY (selectionID)
);

CREATE TABLE Options(
    optionID INT NOT NULL AUTO_INCREMENT, 
    initiativeID INT,
    optionTitle VARCHAR(50),
    boardApproved BOOLEAN,
    descriptionField VARCHAR(8000),
    PRIMARY KEY (optionID)
);


ALTER TABLE Voters ADD FOREIGN KEY (societyID) REFERENCES Society(societyID);

ALTER TABLE Admins ADD FOREIGN KEY (societyID) REFERENCES Society(societyID);

ALTER TABLE Election ADD FOREIGN KEY (societyID) REFERENCES Society(societyID);

ALTER TABLE Roles ADD FOREIGN KEY (electionID) REFERENCES Election(electionID);

ALTER TABLE CandidateRole ADD FOREIGN KEY (candidateID) REFERENCES Candidate(candidateID);

ALTER TABLE CandidateRole ADD FOREIGN KEY (roleID) REFERENCES Roles(roleID);

ALTER TABLE BallotVote ADD FOREIGN KEY (selectionID) REFERENCES OptionInitiative(selectionID);

ALTER TABLE BallotVote ADD FOREIGN KEY (selectionID) REFERENCES CandidateRole(selectionID);

ALTER TABLE Initiative ADD FOREIGN KEY (electionID) REFERENCES Election(electionID);

ALTER TABLE OptionInitiative ADD FOREIGN KEY (initiativeID) REFERENCES Initiative (initiativeID);

ALTER TABLE OptionInitiative ADD FOREIGN KEY (optionID) REFERENCES Options (optionID);

INSERT INTO americandreamelect.society(societyName, logo) VALUES ("Cool Society", "no logo");

INSERT INTO admins(societyID, fName, lName, email, credential1, credential2) VALUES (1, "Ryan", "Vay", "rxv7131@rit.edu", "rxv7131", 123456);

INSERT INTO voters(voterID, societyID, fName, lName, email, credential1, credential2, canVote) VALUES (1, 1, "Ryan", "Vay", "rxv7131@rit.edu", "rvay", "123456", 1);
INSERT INTO voters(voterID, societyID, fName, lName, email, credential1, credential2, canVote) VALUES (2, 1, "Evan", "Vay", "evanvay@test.com", "evay", "123456", 0);