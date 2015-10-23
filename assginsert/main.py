import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import csv
import time
import cloudstorage
import jinja2
from google.appengine.api import app_identity
from cloudstorage import storage_api

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])

# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'adv-database-1:assginment2'

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Connecting to MySQLdb cloud database
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='earthquakes', user='root', charset='utf8', passwd='root1234')
            
        else:
            db = MySQLdb.connect(host='76.183.83.23', port=3306, db='earthquakes', user='root', charset='utf8', passwd='root1234')
            
        
       # Create a list of earthquake entries to render with the HTML.
        earthquake_data1 = [2,3,4,5,6,7]
        earthquake_data2 = [2.99,3.99,4.99,5.99,6.99,7.99]
        place = ['California', 'Nepal', 'Washington', 'India', 'Chile', 'Hawaii', 'Japan']
                 
        variables = {'earthquake_data1': earthquake_data1,'earthquake_data2':earthquake_data2,'place':place}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(variables))
        db.commit()
        db.close()

        
class Guestbook(webapp2.RequestHandler):
    def post(self):

        magnitude1 = self.request.get("mag_data1")
        magnitude2 = self.request.get("mag_data2")
        place = self.request.get("place")
        # Handle the post to create a new guestbook entry.
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='earthquakes', user='root', charset='utf8', passwd='root1234')
        else:
            db = MySQLdb.connect(host='76.183.83.23', port=3306, db='earthquakes', user='root', charset='utf8')
        
        cursor = db.cursor()
        
        query(str(magnitude1),str(magnitude2),place,cursor,self)
        
        
application = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)

                              
def query(mag1,mag2,place,cursor,self):

    
    self.response.write("<html></body>")
    self.response.write("<br>")
    self.response.write("\nWeek1\n")
    self.response.write("<br>")
    s1 = time.clock()
    cursor.execute("select * from all_month where mag between '"+mag1+"' and '"+mag2+"' and time between '2015-05-14T00:00:00Z' and '2015-05-21T23:59:00Z' and type='earthquake' and place like '%"+place+"%'")
    self.response.write("Number of earthquakes for the magnitude :\n" +mag1+"and "+mag2)
    self.response.write("<br>")
    row1 = cursor.fetchall()
    self.response.out.write(len(row1))
    e1 = time.clock()
    t1 = e1-s1
    self.response.write("<br>")
    self.response.write("\nTime taken to execute :\n")
    self.response.write(t1)
    self.response.write("<br>")
   
    self.response.write("\nWeek2\n")
    s2 = time.clock()
    cursor.execute("select * from all_month where mag between '"+mag1+"' and '"+mag2+"' and time between '2015-05-22T00:00:00Z' and '2015-05-28T23:59:00Z' and type ='earthquake'  and place like '%"+place+"%'")
    self.response.write("<br>")
    self.response.write("Number of earthquakes for the magnitude :\n" +mag1+"and "+mag2)
    row2 = cursor.fetchall()
    self.response.write("<br>")
    self.response.out.write(len(row2))
    e2 = time.clock()
    t2 = e2-s2
    self.response.write("<br>")
    self.response.write("\nTime taken to execute :\n")
    self.response.write(t2)
    
    self.response.write("<br>")
    self.response.write("\nWeek3\n")
    s3 = time.clock()
    self.response.write("<br>")
    cursor.execute("select * from all_month where mag between '"+mag1+"' and '"+mag2+"' and time between '2015-05-29T00:00:00Z' and '2015-06-04T23:59:00Z' and type='earthquake'  and place like '%"+place+"%'")
    self.response.write("Number of earthquakes for the magnitude :\n" +mag1+"and "+mag2)
    self.response.write("<br>")
    row3 = cursor.fetchall()
    self.response.out.write(len(row3))
    e3 = time.clock()
    t3 = e3-s3
    self.response.write("<br>")
    self.response.write("\nTime taken to execute :\n")
    self.response.write(t3)
    
    self.response.write("<br>")
    self.response.write("\nWeek4\n")
    s4 = time.clock()
    self.response.write("<br>")
    cursor.execute("select * from all_month where mag between '"+mag1+"' and '"+mag2+"' and time between '2015-06-05T00:00:00Z' and '2015-06-13T23:59:00Z' and type='earthquake'  and place like '%"+place+"%'")
    self.response.write("Number of earthquakes for the magnitude :\n" +mag1+"and "+mag2)
    self.response.write("<br>")
    row4 = cursor.fetchall()
    self.response.out.write(len(row4))
    e4 = time.clock()
    t4 = e4-s4
    self.response.write("<br>")
    self.response.write("\nTime taken to execute :\n")
    self.response.write(t4)
    self.response.write("</body></html>")
  
    
def main():
    application = webapp2.WSGIApplication([('/', MainPage),
                                           ('/sign', Guestbook)],
                                          debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()