# Codeforces-AC-Submissions-Downloader
Downloading AC Submisison files for a given user handle from Codeforces Platform using Scrapy Framework in Python.

Folder named updated_on_1_mar_2018 contains the latest version of Codeforces-AC-Submissions-Downloader
A web interface has been implemented at localhost level using Flask Framework.

Follow these steps to download your accepted submissions of Codeforces Platform

1. Changes in the path:
    Change the path where the submissions files willbe downloaded accordingly !!!
    Open the final_get_cf_sub_using_cf_api.py in the spider folder ... change the path wherever mentioned as a comment
    according to your system!!!
    
2. Launch the Flask Server:
    In updated_on_1_mar_2018 launch the terminal and run command < python3 integrator_flask_scrapy.py >
    Flask Server launched!

3. Go to Browser and open http://localhost:5000

4. Type the valid Codeforces Handle in the <_enter_cf_handle_> bar and press the submit button.
   Now relax for some time or let yourself do something else work ... 
   
5. Once the script get executed and completed go to folder named Codeforces again go to nested folder AC_SUBMISSIONS ... here      you will find all your AC submissions named according to ContestId+Index+Problem_Name !!!

6. For any suggestions or doubt feel free to contact! Links provided at the bottom of the Web Page!!! 
