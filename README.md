# GitHub Issue Events Crawler

A crawler for querying issue timeline events of GitHub Repositories


-----------timeline_events_crawler (saved to local files:

                Input repo_slug list


❗️❗️❗️ Reminder: check the input repo list to ensure that there is no additional empty line at the bottom ❗️❗️❗️


-----------timeline_events_crawler_mysql (saved to database server:

                repo_list folder: 
                        first generate repo_list table by 1. create repo_list table.sql -> 
                                                             import morethan500pr.csv file -> 
                                                             repo_list.py
                                                             
                                                       or 2. by create repo_list table.sql -> 
                                                             insert repo_list morethan500pr query.sql

 ❗️❗️❗️ Reminder: fill in  the schema and table name in the sql insert query
                   
![image](https://user-images.githubusercontent.com/90332805/175976692-58e9e92e-c723-43d2-9112-ae81c8ae5fab.png)

 ❗️❗️❗️ Note that repo_list and issue_pr_event table contents may not be consistent if table structure changed by scripts. (eg. new columns)
       Then you need to rebuild the table by create...sql file and insert contents by scripts
