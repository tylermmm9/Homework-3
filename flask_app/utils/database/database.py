import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path="flask_app/database/"):
        if purge == True:
            return
        self.purge = True
        files = [data_path + "create_tables/institutions.sql",
                data_path + "create_tables/positions.sql",
                data_path + "create_tables/experiences.sql",
                data_path + "create_tables/skills.sql",
                data_path + "create_tables/users.sql"]  # ← Add this line

                 
        for file in files:
            fp = open(file, "r")
            stmt = fp.read()
            row = self.query(stmt)

        inst_ids = [int(row['inst_id']) for row in self.query("SELECT inst_id FROM institutions")]
        csv_reader = csv.reader(open(data_path + "initial_data/" + "institutions.csv"))
        columns = next(csv_reader)
        data = []
        for line in csv_reader:
            print("institutions")
            data.append(line)
        self.insertRows("institutions", columns, data)

        pos_ids = [int(row['position_id']) for row in self.query("SELECT position_id FROM positions")]
        csv_reader = csv.reader(open(data_path + "initial_data/" + "positions.csv"))
        columns = next(csv_reader)
        data = []
        for line in csv_reader:
            print("position")
            data.append(line)
        self.insertRows("positions", columns, data)



        exper_ids = [int(row['experience_id']) for row in self.query("SELECT experience_id FROM experiences")]
        csv_reader = csv.reader(open(data_path + "initial_data/" + "experiences.csv"))
        columns = next(csv_reader)
        data = []
        for line in csv_reader:
            print("experience")
            print(line)
            data.append(line)

        self.insertRows("experiences", columns, data)

        skills_ids = [int(row['skill_id']) for row in self.query("SELECT skill_id FROM skills")]
        csv_reader = csv.reader(open(data_path + "initial_data/" + "skills.csv"))
        columns = next(csv_reader)
        data = []
        for line in csv_reader:
            print("skill")
            data.append(line)
        self.insertRows("skills", columns, data)

    def clearTables(self):
        tables = ["skills", "experiences", "positions", "institutions"]

        for table in tables:
            query = f"DELETE FROM {table};"
            self.query(query)





    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        #Setting frmt to INSERT IGNORE INTO `institutions` for example
        frmt = "INSERT INTO `{}` (".format(table)

        #For each column add all of the values to that column
        #INSERT IGNORE INTO `institutions` (`inst_id`,`type`,`name`,`department`,`address`,`city`,`state`,`zip`) Values(
        for val in columns: frmt += "`{}`,".format(val)
        frmt = frmt[:len(frmt)-1] + ") VALUES "

        #Values will then become
        #Values ("1","Academia","Michigan State University","Computer Science",NULL,"East Lansing","Michigan",NULL);
        for lst in parameters:
            frmt += "("
            for val in lst:
                frmt += "'{}', ".format(val)
            frmt = frmt[:len(frmt)-2] + ("),")
        frmt = frmt[:len(frmt)-1] + ";"

        existing_inst = self.query(f"SELECT {columns[0]} FROM `{table}`")
        existing = [val[f'{columns[0]}'] for val in existing_inst]
        if table != 'feedback' and [int(val[0]) for val in parameters] == existing:
            return
        self.query(frmt)


    def getResumeData(self):
        resume_data = {
            "name": "Tyler Murray",
            "location": "East Lansing, MI",
            "contact": {
                "email": "murra381@msu.edu",
                "phone": "(561) 306-1494",
                "linkedin": "https://www.linkedin.com/in/tyler-murray-7026ab1b8/"
            },
            "objective": "To leverage my knowledge of information management systems and cloud computing methodologies in software application development and gain relevant experience in related fields.",
            "education": [
                {
                    "institution": "Michigan State University",
                    "degree": "Bachelor of Science, Computer Science",
                    "gpa": "3.2",
                    "dates": "May 2026"
                }
            ],
            "experience": [
                {
                    "title": "Expansion Intern",
                    "company": "Triangle National Headquarters",
                    "location": "Allendale, MI",
                    "dates": "September 2024 - Present",
                    "responsibilities": [
                        "Virtually sourced and engaged with over 100 potential new members weekly to establish a new colony at Grand Valley State University, Texas A&M University, and University of Toledo.",
                        "Coordinated with the Director of Strategic Growth in weekly one-on-one meetings to discuss recruitment strategies and progress.",
                        "Utilized ChapterBuilder software to manage and track outreach efforts, ensuring accurate and up-to-date records of all candidate interactions."
                    ]
                },
                {
                    "title": "Service Center Representative",
                    "company": "Michigan State University RHS",
                    "location": "East Lansing, MI",
                    "dates": "September 2023 - August 2024",
                    "responsibilities": [
                        "Provided routine clerical support within a reception hall area and served as a friendly face to residents.",
                        "Answered phones, processed mail and packages, assisted in maintaining records and accounts.",
                        "Assured in-house residence hall security and customer service throughout day/night."
                    ]
                },
                {
                    "title": "Administrative Assistant Intern",
                    "company": "Plumosa School of the Arts",
                    "location": "Delray Beach, FL",
                    "dates": "June 2023 - August 2023",
                    "responsibilities": [
                        "Offered aid to school administration in any task required, including support with ASD and children on the spectrum.",
                        "Sorted books, copied papers, and delivered materials to classrooms for teachers and administrators.",
                        "Assisted teachers in classrooms as needed and helped guide classroom activities."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Texas Lawmakers API Newspaper",
                    "location": "East Lansing, MI",
                    "dates": "January 2025 - Present",
                    "description": [
                        "Designing and implementing an AI-driven personalized newsletter platform that aggregates, curates, summarizes, and delivers high-quality, niche-specific news to Texas Lawmakers.",
                        "Leveraged advanced AI tools, automation workflows, and user feedback to ensure relevance, engagement, and scalability.",
                        "Currently working with a lobbyist to secure a government contract to distribute the finished product to 400 Texas Lawmakers."
                    ]
                }
            ],
            "technical_skills": {
                "programming_languages": ["ARM Assembly", "C", "C++", "CSS", "HTML", "JavaScript", "Python", "SQL"],
                "software_knowledge": ["VS Code", "PyCharm", "CLion", "Vim", "PuTTy", "SQLite", "Microsoft Office", "Google Workspace", "MIT App Inventor"],
                "operating_systems": ["Windows", "Unix"]
            }
        }

        return resume_data
    def addFeedback(self, feedback):
        # Determines if create tables has been created
        comment_id = 1
        try:
            results = self.query("""SELECT * from feedback""")
            comment_id = len(results) + 1
            print(results)
        except:
            data_path= "flask_app/database/" + "create_tables/" + "feedback.sql"
            fp = open(data_path, "r")
            stmt = fp.read()
            row = self.query(stmt)
        feedback = [[comment_id] + feedback]
        self.insertRows("feedback", ['comment_id','name', 'email', 'comment'], feedback)
    def GetFeedbackData(self):
        query = """
        SELECT
        feedback.name AS name,
        feedback.email AS email,
        feedback.comment AS comment
        FROM feedback"""
        try:
            results = self.query(query)
            return results
        except:
            return []

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        # create a new database cursor
        test_cursor = self.query("SELECT * FROM users WHERE email = %s", (email,))
        
        if test_cursor:
            return {"success": False, "error": "User already exists"}

        # encrypt password
        encrypted_password = self.onewayEncrypt(password)

        # insert new user into database
        self.query(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            (email, encrypted_password, role)
        )
        return {"success": True}

    def authenticate(self, email='me@email.com', password='password'):
        # gets table of users
        user_table = self.query("SELECT password, role FROM users WHERE email = %s", (email,))

        if not user_table:
            return {"success": False, "error": "User does not exist"}

        # encrypt password
        encrypted_password = self.onewayEncrypt(password)
        stored_password = user_table[0]['password']

        # check password
        if encrypted_password != stored_password:
            return {"success": False, "error": "Incorrect password"}

        # return role
        return {"success": True, "role": user_table[0]['role']}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


