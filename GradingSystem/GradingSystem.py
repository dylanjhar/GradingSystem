def main():
    #Open files that contain the data needed to be read
    rawTests = open('rawTests.txt', 'r')
    students = open('students.txt', 'r')
    
    #Create files to output data to
    gradeData = open('gradeData.txt', 'w')
    errors = open('errors.txt', 'w')
    
    #2D List [ID][Answers]
    testData = getTestData(rawTests)
    #2D List [ID][Name]
    studentData = getStudentData(students)

    answerKey = testData[0][1]

    gradeData.write('First Name\tLast Name\t\tScore\tGrade\n')
    gradeData.write('=========================================\n')

    for test in testData[1:]:
        IDValCheck(test, errors)
        gradeTest(test, answerKey)
        assignLetterGrade(test)
        assaignName(test, studentData, errors)
        gradeOutput(test, gradeData)

    #Close open files
    rawTests.close()
    students.close()
    gradeData.close()
    errors.close()

#getStudentData takes the rawTests file and creates a 2D list
#[ID][Answers]
def getTestData(testFile):
    testData = []
    y = 0
    for line in testFile:
        testData.append([])
        line = line.rstrip('\n')
        IDSep = line.split(';')
        for ch in IDSep:
            testData[y].append(ch)
        y += 1
    return testData

#getStudentData takes the students file and creates a 2D list
#[ID][Name]
def getStudentData(studentFile):
    studentData = []
    y = 0
    for line in studentFile:
        studentData.append([])
        line = line.rstrip('\n')
        IDSep = line.split(' ')
        for ch in IDSep:
            studentData[y].append(ch)
        y += 1
    return studentData

#IDValCheck takes the test, the error file
#and writes invalid IDs to the error file
def IDValCheck(test, errorFile):
    ID = test[0]
    if len(ID) != 6:
        errorFile.write(f'{ID} is invalid - Improper length\n')
    elif not ID[:2].isalpha():
        errorFile.write(f'{ID} is invalid - First two characters are not both letters\n')
    elif ID[0] == ID[1]:
        errorFile.write(f'{ID} is invalid - First two characters are not unique\n')
    elif not ID[2:6].isdigit():
        errorFile.write(f'{ID} is invalid - Last four characters are not all numbers\n')
    for num in ID[2:6]:
        if ID.count(num) > 1:
            errorFile.write(f'{ID} is invalid - Duplicate digits\n')
            break

#gradeTest takes the test, the answer key
#and appends the score to the student's ID
#[ID][Score]
def gradeTest(test, answerKey):
    studentAnswers = test[1]
    score = 0
    ch = 0
    for answer in answerKey:
        if studentAnswers[ch] == answer:
            score += 1
        elif studentAnswers[ch] != answer and studentAnswers[ch] != ' ':
            score -= 0.25
        ch += 1
    del test[1]
    test.append(format(score, '.2f'))
    return test
        
#assignGrade takes the test
#and appends the letter grade that corresponds with the test score
#[ID][Score][Grade]
def assignLetterGrade(test):
    score = float(test[1])
    if score > 46:
        test.append('A')
    elif score >= 44:
        test.append('A-')
    elif score >= 42:
        test.append('B+')
    elif score >= 40:
        test.append('B')
    elif score >= 38:
        test.append('B-')
    elif score >= 36:
        test.append('C+')
    elif score >= 34:
        test.append('C')
    elif score >= 32:
        test.append('C-')
    elif score >= 30:
        test.append('D')
    else:
        test.append('F')
    return test
        
#assaignName takes the test, the students file, the error file
#and finds a matching name for the ID, deletes the ID and appends the student's name
#if there is no matching name, the test is removed from the list and written to the error file
#[First name][Last name][Grade][Score]
def assaignName(test, studentData, errorFile):
    IDScore = test[0]
    score = test[1]
    grade = test[2]
    y = 0
    for _ in studentData:
        officialID = studentData[y][0]
        if officialID == IDScore:
            del test[0]
            test.append(studentData[y][2])
            test.append(studentData[y][1])
            test.reverse()
            return test
            break
        y += 1
    if IDScore[2:6].isdigit():
        errorFile.write(f'ID: {IDScore} - No name found {score} {grade}\n')

#gradeOutput takes the test, the output file
#and writes the test to the output file
def gradeOutput(test, outFile):
    if not any(ch.isdigit() for ch in test[0]):
        first = format(str(test[0]), '10')
        last = format(str(test[1]), '10')
        score = format(float(test[3]), '5.2f')
        grade = str(test[2])
        outFile.write(f'{first}\t{last}\t\t{score}\t{grade}\n')

main()
