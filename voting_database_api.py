import datetime
from datetime import datetime
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password' #change to yours
app.config['MYSQL_DB'] = 'americandreamelect'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'cred1' in request.form and 'cred2' in request.form:
        credential1 = request.form['cred1']
        credential2str = request.form['cred2']
        credential2 = None
        if credential2str != '':
            credential2 = int(credential2str)
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM admins WHERE credential1 = %s AND credential2 = %s"
        val = (credential1, credential2)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        if account:
            msg = 'Logged in successfully.'
            return render_template('admin_create.html', msg = msg)
        elif account == None:
            sql = "SELECT * FROM voters WHERE credential1 = %s AND credential2 = %s"
            val = (credential1, credential2)
            mycursor.execute(sql, val)
            account = mycursor.fetchone()
            if account:
                if account['canVote'] == 1:
                    #msg = 'Logged in successfully.'
                    ballotString = create_ballot()
                    return render_template('ballot.html', ballotString = ballotString)
                else:
                    msg = 'You do not have permission to vote.'
            else:
                msg = 'Invalid credentials.'
        else:
            msg = 'Invalid credentials.'
    return render_template('login.html', msg = msg)

@app.route('/admin_create',methods = ['POST', 'GET'])
def admin_create():
    msg = ''
    if request.method == 'POST' and 'societyId' in request.form and 'title' in request.form and 'startDate' in request.form and 'endDate' in request.form and 'information' in request.form:
        societyIdStr = request.form['societyId']
        electionTitle = request.form['title']
        startDateStr = request.form['startDate']
        endDateStr = request.form['endDate']
        information = request.form['information']
        startDate = None
        endDate = None
        societyId = None
        if societyIdStr == '' and electionTitle == '' and startDateStr == '' and endDateStr == '' and information == '':
            msg = "All fields must be filled."
        else:
            if societyIdStr != '':
                societyId = int(societyIdStr)
            if startDateStr != '':
                startDate = datetime.strptime(startDateStr, '%Y-%m-%d').date()
            if endDateStr != '':
                endDate = datetime.strptime(endDateStr, '%Y-%m-%d').date()
            msg = create_election(societyId, electionTitle, startDate, endDate, information)
    elif request.method == 'POST':
        msg = "All fields must be filled."
    return render_template('admin_create.html', msg = msg)

@app.route('/ballot', methods = ['POST', 'GET'])
def ballot():
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    msg = ''
    #fieldTitle = request.headers.get("h2");
    if request.method == 'POST':
        ballotId = create_ballot_complete()

        sql = "SELECT MAX(electionID) FROM Election"
        mycursor.execute(sql)
        maxElection = mycursor.fetchone()['MAX(electionID)']

        #create_ballot_role_vote(ballotId, maxElection)
        #create_ballot_initiative_vote(ballotId, maxElection)

        sql = f"SELECT * FROM Roles WHERE electionId = {maxElection}"
        mycursor.execute(sql)
        roleCount = mycursor.rowcount
        roleList = mycursor.fetchall()
        print(roleCount)
        testNum = 0
        for x in roleList:
            testNum += 1
            print("TestNum: " + str(testNum))
            fieldTitle = x["roleTitle"]
            currentRole = 1
            while currentRole <= roleCount:
                roleName = "role" + str(currentRole)
                print(roleName)
                selectedCandidate = request.form[roleName]
                candidateNum = int(selectedCandidate)
                print(fieldTitle)
                print(candidateNum)
                sql = f"INSERT INTO BallotVote(ballotId, fieldTitle, candidateId) VALUES ({ballotId}, \"{str(fieldTitle)}\", {candidateNum})"
                print(sql)
                print("Going to execute...")
                mycursor.execute(sql)
                sql = "SELECT * FROM BallotVote"
                mycursor.execute(sql)
                #mysql.connection.commit()
                print(mycursor.fetchone())
                print("Executed.")
                currentRole += 1

        sql = f"SELECT * FROM Initiative WHERE electionId = {maxElection}"
        mycursor.execute(sql)
        initiativeCount = mycursor.rowcount
        initiativeList = mycursor.fetchall()
        for x in initiativeList:
            fieldTitle = x["initiativeTitle"]
            currentInitiative = 1
            while currentInitiative <= initiativeCount:
                initiativeName = "initiative" + str(currentInitiative)
                selectedOption = request.form[initiativeName]
                optionNum = int(selectedOption)
                sql = f"INSERT INTO BallotVote(ballotId, fieldTitle, optionId) VALUES ({ballotId}, \"{str(fieldTitle)}\", {optionNum})"
                mycursor.execute(sql)
                mysql.connection.commit()
                currentInitiative += 1

    return render_template('ballotconfirmation.html', msg = msg)

def create_ballot():
    ballotString = ""
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT MAX(electionID) FROM Election"
    mycursor.execute(sql)
    maxElection = mycursor.fetchone()['MAX(electionID)']
    print(maxElection)
    #maxElectionID = maxElection['MAX(electionID)']
    #print(maxElectionID)
    sql = f"SELECT electionTitle FROM Election WHERE electionId = {maxElection}"
    mycursor.execute(sql)
    electionTitle = mycursor.fetchone()
    ballotString = "<h2 name=\"h2\">" + electionTitle['electionTitle'] + "</h2>"

    sql = f"SELECT * FROM Roles WHERE electionId = {maxElection}"
    mycursor.execute(sql)
    roleFields = mycursor.fetchall()
    roleNum = 0
    for x in roleFields:
        roleNum += 1
        ballotString = ballotString + "<p><b>" + x["roleTitle"] + "</b></p>"
        roleId = x["roleID"]
        sql = f"SELECT * FROM CandidateRole WHERE roleId = {roleId}"
        mycursor.execute(sql)
        candidateRoleFields = mycursor.fetchall()
        candidateNum = 0
        for y in candidateRoleFields:
            #print(y)
            candidateNum = candidateNum + 1
            ballotString = ballotString + "<input type=\"radio\" id=\"candidate" + str(candidateNum) +"\" name=\"role" + str(roleNum) + "\" value=\"" + str(candidateNum) + "\">"
            candidateId = y["candidateID"]
            sql = f"SELECT * FROM Candidate WHERE candidateId = {candidateId}"
            mycursor.execute(sql)
            candidateFields = mycursor.fetchone()
            ballotString = ballotString + "<label for=\"candidate" + str(candidateNum) + "\">" + candidateFields["fName"] + " " + candidateFields["midInitial"] \
                + ". " + candidateFields["lName"] + "</label><br>"

    sql = f"SELECT * FROM Initiative WHERE electionId = {maxElection}"
    mycursor.execute(sql)
    initFields = mycursor.fetchall()
    initiativeNum = 0
    for x in initFields:
        initiativeNum += 1
        ballotString = ballotString + "<p><b>" + x["initiativeTitle"] + "</b></p>"
        initiativeId = x["initiativeID"]
        sql = f"SELECT * FROM OptionInitiative WHERE initiativeId = {initiativeId}"
        mycursor.execute(sql)
        optionInitiativeFields = mycursor.fetchall()
        optionNum = 0
        for y in optionInitiativeFields:
            optionNum = optionNum + 1
            ballotString = ballotString + "<input type=\"radio\" id=\"option" + str(optionNum) +"\" name=\"initiative" + str(initiativeNum) + "\" value=\"" + str(optionNum) + "\">"
            optionId = y["optionID"]
            sql = f"SELECT * FROM Options WHERE optionId = {optionId}"
            mycursor.execute(sql)
            optionFields = mycursor.fetchone()
            ballotString = ballotString + "<label for=\"option" + str(optionNum) + "\">" + optionFields["optionTitle"] + "</label><br>"
    
    ballotString = ballotString + "<br></br>"
    ballotString = ballotString + "<input type=\"submit\" value=\"SUBMIT\" />"
    #print(ballotString)
    return ballotString

def create_election(societyId, electionTitle, startDate, endDate, information):
    sql = "INSERT INTO Election (societyId, electionTitle, startDate, endDate, information) VALUES (%s, %s, %s, %s, %s)"
    val = (societyId, electionTitle, startDate, endDate, information)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    msg = "Election successfully created, ID is " + str(mycursor.lastrowid)
    return msg

def select_election(electionId):
    sql = f"SELECT * FROM Election WHERE electionId = {electionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    electionSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected election.")
    return electionSelect

def update_election(electionTitle, startDate, endDate, information, electionId):
    sql = f"UPDATE Election SET electionTitle = {electionTitle}, startDate = {startDate}, endDate = {endDate}, information = {information} \
        WHERE electionId = {electionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Election successfully updated.")

def delete_election(electionId):
    sql = f"DELETE FROM Election WHERE electionId = {electionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Election successfully deleted.")

def create_role(roleTitle, roleDescription, votingType):
    #roleTitle = input("Enter role title: ")
    #roleDescription = input("Enter a description for the role: ")
    #votingType = int(input("Enter the number for the voting type for this role (1 - single choice, 2 - multi choice, 3 - ranked choice):"))
    sql = "INSERT INTO Roles (roleTitle, roleDescription, votingType) VALUES (%s, %s, %s)"
    val = (roleTitle, roleDescription, votingType)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Role successfully created, ID is ", mycursor.lastrowid)

def select_role(roleId):
    sql = f"SELECT * FROM Role WHERE roleId = {roleId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    roleSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected role.")
    return roleSelect

def delete_role(roleId):
    sql = f"DELETE FROM Roles WHERE roleId = {roleId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Role successfully deleted.")

def create_candidate_role(roleTitle, candidateId, roleId, candStatement):
    sql = "INSERT INTO CandidateRole (roleTitle, candidateId, roleId, candStatement) VALUES (%s, %s, %s, %s)"
    val = (roleTitle, candidateId, roleId, candStatement)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Candidate successfully nominated for role, ID is ", mycursor.lastrowid)

def select_candidate_role(selectionId):
    sql = f"SELECT * FROM CandidateRole WHERE selectionId = {selectionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    candidateRoleSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected role nomination.")
    return candidateRoleSelect

def delete_candidate_role(selectionId):
    sql = f"DELETE FROM CandidateRole WHERE selectionId = {selectionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Candidate removed from nomination.")

def create_candidate(fName, midInitial, lName, picture, position, proBackground, bio):
    sql = "INSERT INTO Candidate (fName, midInitial, lName, picture, position, proBackground, bio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (fName, midInitial, lName, picture, position, proBackground, bio)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Candidate successfully created, ID is ", mycursor.lastrowid)

def select_candidate(candidateId):
    sql = f"SELECT * FROM Candidate WHERE candidateId = {candidateId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    candidateSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected candidate.")
    return candidateSelect

def update_candidate(fName, midInitial, lName, picture, position, proBackground, bio, candidateId):
    sql = "UPDATE Candidate SET fName = %s, midInitial = %c, lName = %s, picture = %s, position = %s, proBackground = %s, bio = %s \
        WHERE candidateId = %s"
    val = (fName, midInitial, lName, picture, position, proBackground, bio, candidateId)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Candidate successfully updated.")

def delete_candidate(candidateId):
    sql = f"DELETE FROM Candidate WHERE candidateId = {candidateId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Candidate successfully deleted.")

def create_initiative(initiativeTitle, initiativeDescription, votingType):
    #initiativeTitle = input("Enter initiative title: ")
    #initiativeDescription = input("Enter a description for the initiative: ")
    #votingType = int(input("Enter the number for the voting type for this initiative (1 - single choice, 2 - multi choice, 3 - ranked choice):"))
    sql = "INSERT INTO Initiative (initiativeTitle, initiativeDescription, votingType) VALUES (%s, %s, %s)"
    val = (initiativeTitle, initiativeDescription, votingType)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Initiative successfully created, ID is ", mycursor.lastrowid)

def select_initiative(initiativeId):
    sql = f"SELECT * FROM Initiative WHERE initiativeId = {initiativeId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    initiativeSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected initiative.")
    return initiativeSelect

def delete_initiative(initiativeId):
    #initiativeId = input("Enter the ID of the initiative to delete: ")
    sql = f"DELETE FROM Initiative WHERE initiativeId = {initiativeId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Initiative successfully deleted.")

def create_option_initiative(initiativeTitle, initiativeId, optionId):
    sql = "INSERT INTO OptionInitiative (initiativeTitle, initiativeId, optionId) VALUES (%s, %s, %s)"
    val = (initiativeTitle, initiativeId, optionId)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Option successfully entered in initiative, ID is ", mycursor.lastrowid)

def select_option_initiative(selectionId):
    sql = f"SELECT * FROM OptionInitiative WHERE selectionId = {selectionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    optionInitiativeSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected initiative nomination.")
    return optionInitiativeSelect

def delete_option_initiative(selectionId):
    sql = f"DELETE FROM OptionInitiative WHERE selectionId = {selectionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Option removed from initiative nomination.")

def create_option(optionTitle, boardApproved, description):
    #optionTitle = input("Enter option title: ")
    #boardApproved = input("Enter if this option is board approved (0 for no, 1 for yes): ")
    #description = input("Enter a description for this option: ")
    sql = "INSERT INTO Option (optionTitle, boardApproved, description) VALUES (%s, %d, %s)"
    val = (optionTitle, boardApproved, description)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Option successfully created, ID is ", mycursor.lastrowid)

def select_option(optionId):
    sql = f"SELECT * FROM Option WHERE optionId = {optionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    optionSelect = mycursor.fetchone()
    mysql.connection.commit()
    print("Returning selected option.")
    return optionSelect

def update_option(optionTitle, boardApproved, description, optionId):
    sql = "UPDATE Option SET optionTitle = %s, boardApproved = %d, description = %s \
        WHERE optionId = %d"
    val = (optionTitle, boardApproved, description, optionId)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Option successfully updated.")

def delete_option(optionId):
    sql = f"DELETE FROM Option WHERE optionId = {optionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Option successfully deleted.")

def cast_role_vote(roleId, candidateId):
    sql = f"SELECT RoleTitle, selectionId FROM candidateRole WHERE roleId = {roleId} AND candidateId = {candidateId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    voteRoleTitle = mycursor.fetchone()[0]
    voteSelectionId = mycursor.fetchone()[1]
    sql = f"INSERT INTO ballotVote (fieldTitle, selectionId) VALUES ({voteRoleTitle}, {voteSelectionId})"
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Vote was cast, vote ID is ", mycursor.lastrowid)

def cast_initiative_vote(initiativeId, optionId):
    sql = f"SELECT InitiativeTitle, selectionId FROM initiativeOption WHERE roleId = {initiativeId} AND candidateId = {optionId}"
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql)
    voteInitiativeTitle = mycursor.fetchone()[0]
    voteSelectionId = mycursor.fetchone()[1]
    sql = f"INSERT INTO ballotVote (fieldTitle, selectionId) VALUES ({voteInitiativeTitle}, {voteSelectionId})"
    mycursor.execute(sql)
    mysql.connection.commit()
    print("Vote was cast, vote ID is ", mycursor.lastrowid)

def create_ballot_complete():
    dateCast = datetime.now()
    sql = "INSERT INTO Ballot (dateCast) VALUES (%s)"
    #val = (dateCast)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, [dateCast])
    mysql.connection.commit()
    print("Ballot successfully created, ID is ", mycursor.lastrowid)
    return(mycursor.lastrowid)

def create_society(societyName, logo):
    sql = "INSERT INTO Society (societyName, logo) VALUES (%s, %s)"
    val = (societyName, logo)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Society successfully created, ID is ", mycursor.lastrowid)

def create_voter(voterId, societyId, fName, lName, email, credential1, credential2, canVote):
    #sql = f"INSERT INTO Voters (voterId, societyId, fName, lName, email, credential1, credential2, canVote) VALUES \
    #    ({voterId} {societyId}, {fName}, {lName}, {email}, {credential1}, {credential2}, {canVote})"
    sql = "INSERT INTO Voters (voterId, societyId, fName, lName, email, credential1, credential2, canVote) VALUES \
        (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (voterId, societyId, fName, lName, email, credential1, credential2, canVote)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Voter successfully created, ID is ", voterId)

def create_admin(societyId, fName, lName, email, credential1, credential2):
    sql = "INSERT INTO Admins (societyId, fName, lName, email, credential1, credential2) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (societyId, fName, lName, email, credential1, credential2)
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute(sql, val)
    mysql.connection.commit()
    print("Admin successfully created, ID is ", mycursor.lastrowid)

#mycursor.execute("USE americanDreamElect")
#if __name__ == '__main__':
#  app.run(debug=True)

if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"))