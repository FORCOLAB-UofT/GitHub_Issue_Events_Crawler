# GitHub Issue Events Crawler

A crawler for querying issue timeline events of GitHub Repositories


-----------timeline_events_crawler (saved to local files:

                Input repo_slug list


       Reminder: check the input repo list to ensure that there is no additional empty line at the bottom ❗️❗️❗️


-----------timeline_events_crawler_mysql (saved to database server:

                repo_list folder: 
                        first generate repo_list table by 1. create repo_list table.sql -> 
                                                             import morethan500pr.csv file -> 
                                                             repo_list.py
                                                             
                                                       or 2. by create repo_list table.sql -> 
                                                             insert repo_list morethan500pr query.sql
                                                             
 ❗️❗️❗️ Note that repo_list and issue_pr_event table contents may not be consistent if table structure changed by scripts. (eg. new columns)
       Then you need to rebuild the table by create...sql file and insert contents by scripts
       
       
       
 📝 Reminder: fill in or change the schema and table name in the sql insert query
                  
( in search_cross_ref.py ⬇️)

<img width="941" alt="Screen Shot 2022-06-29 at 5 09 49 AM" src="https://user-images.githubusercontent.com/90332805/176300153-3d5ee578-3733-4322-a70c-b09d466042b0.png">
                  
                  
( in repo_list.py ⬇️)  

<img width="941" alt="Screen Shot 2022-06-29 at 5 10 22 AM" src="https://user-images.githubusercontent.com/90332805/176290219-8559daec-1db9-44c4-ae89-df324996dbf1.png">
                  
                  
( in timeline_crawler_mysql.py ⬇️)   

<img width="801" alt="Screen Shot 2022-06-29 at 5 11 02 AM" src="https://user-images.githubusercontent.com/90332805/176290737-5f7918a5-0b8d-4af8-b621-53778f9b01bb.png">
                  

            
### Database connection set up
Create a new python file mySetting.py to store the github api tokens and database connection creditials 
 ![image info](Screenshot_settings.png)
