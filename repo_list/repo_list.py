import mysql.connector

mydb = mysql.connector.connect(
    host='',
    user='',
    password='',
    port='',
    database=''
)

mycursor = mydb.cursor()
mycursor.execute("Insert into new_schema.repo_list (repo_index, repo_name)"
                 "Select ROW_NUMBER() OVER (ORDER BY morethan500pr.repo_id) + (SELECT MAX(repo_index) FROM repo_list)"
                 ", REPLACE(repo_url, 'https://api.github.com/repos/', '') From new_schema.morethan500pr")
mydb.commit()