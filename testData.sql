USE americandreamelect;

INSERT INTO society(societyName, logo) VALUES ("Cool Society", "no logo");

INSERT INTO admins(societyID, fName, lName, email, credential1, credential2) VALUES (1, "Ryan", "Vay", "rxv7131@rit.edu", "rxv7131", 123456);

INSERT INTO voters(voterID, societyID, fName, lName, email, credential1, credential2, canVote) VALUES (1, 1, "Ryan", "Vay", "rxv7131@rit.edu", "rvay", 123456, 1);
INSERT INTO voters(voterID, societyID, fName, lName, email, credential1, credential2, canVote) VALUES (2, 1, "Evan", "Vay", "evanvay@test.com", "evay", 123456, 0);

INSERT INTO Election(societyID, electionTitle, information) VALUES (1, "Test Election", "This is a test election.");

INSERT INTO Roles(electionId, roleTitle, roleDescription, votingType) VALUES (1, "Grand Poobah", "Please vote", 1);
INSERT INTO Roles(electionId, roleTitle, roleDescription, votingType) VALUES (1, "Little Baby Man", "Choose their fate", 1);

INSERT INTO Candidate(fName, midInitial, lName) VALUES ("Ryan", 'N', "Vay");
INSERT INTO Candidate(fName, midInitial, lName) VALUES ("Evan", 'M', "Vay");

INSERT INTO candidaterole(roleTitle, candidateId, roleId) VALUES ("Grand Poobah", 1, 1);
INSERT INTO candidaterole(roleTitle, candidateId, roleId) VALUES ("Grand Poobah", 2, 1);
INSERT INTO candidaterole(roleTitle, candidateId, roleId) VALUES ("Little Baby Man", 1, 2);
INSERT INTO candidaterole(roleTitle, candidateId, roleId) VALUES ("Little Baby Man", 2, 2);

INSERT INTO Initiative(electionID, initiativeTitle, votingType) VALUES (1, "What should we do?", 1);
INSERT INTO Initiative(electionID, initiativeTitle, votingType) VALUES (1, "What should we NOT do?", 1);

INSERT INTO Options(initiativeID, optionTitle) VALUES (1, "Work hard");
INSERT INTO Options(initiativeID, optionTitle) VALUES (1, "Scream and panic");
INSERT INTO Options(initiativeID, optionTitle) VALUES (2, "Work hard");
INSERT INTO Options(initiativeID, optionTitle) VALUES (2, "Scream and panic");

INSERT INTO OptionInitiative(initiativeTitle, initiativeId, optionId) VALUES ("What should we do?", 1, 1);
INSERT INTO OptionInitiative(initiativeTitle, initiativeId, optionId) VALUES ("What should we do?", 1, 2);
INSERT INTO OptionInitiative(initiativeTitle, initiativeId, optionId) VALUES ("What should we NOT do?", 2, 1);
INSERT INTO OptionInitiative(initiativeTitle, initiativeId, optionId) VALUES ("What should we NOT do?", 2, 2);