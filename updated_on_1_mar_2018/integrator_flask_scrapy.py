from flask import Flask, redirect, url_for, render_template, request
import subprocess
import time

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
            
@app.route('/result',methods = ['POST', 'GET'])
def result():
    cf_handle = str(request.form['cf_handle'])
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl final_cf_submissions -a category=<cf_handle> 

    wait for  this command to finish, and read output.json to client.
    """
    spider_name = "final_cf_submissions"
    subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "category="+cf_handle])
    return redirect(url_for('home'))
    #returns cf_handle
    #with open("output.json") as items_file:
    #    return items_file.read()

if __name__ == '__main__':
    app.run(debug=True)

