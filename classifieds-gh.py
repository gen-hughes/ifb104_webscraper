
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 2, 2021.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 110000031 # put your student number here as an integer
student_name   = 'Genevieve Hughes' # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Classified Ads
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a robust, interactive application that allows its user to view
#  and save items currently for sale from multiple online sources.
#
#  See the client's requirements accompanying this file for full
#  details.
#
#--------------------------------------------------------------------#



#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via the "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



# -----Student's Solution---------------------------------------------#

# Put your solution at the end of this file.

# Comments for the functionality can be found on the right side of the code (the widgets are quite long so comments are above them)
# Incognito is used, as sometimes the websites do not work otherwise

#----<GLOBAL VARIABLES>----#

# initialising global array for database entry
db_entry = []

#---------<FUNCTIONS>--------#

# function to open the url of the selected page when 'more details' is selected
    # using variable shop_selection and values from the labels
def showurl():
    if shop_selection.get() == 1:                                                           # ebay url
        urldisplay("https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719")
    elif shop_selection.get() == 2:                                                         # buysearchsell (bss) url
        urldisplay("https://www.buysearchsell.com.au/all-locations/pets/?sort=date")
    elif shop_selection.get() == 3:                                                         # japan today url
        urldisplay("https://classifieds.japantoday.com/index/index/category/appliance")

# function to display the ebay information
def ebay():
    # error trapping is implemented here
    # try the following if there are no errors raised
    try:

        # download the ebay url using inbuilt function       
        ebaydl = download("https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719", incognito=True)           
    
        # regex to find title, cost and description from the source code
        ebayitems = findall(r'<h3 class=\"s-item__title\"\>([^<]+)</h3>[^AU]+(AU \$[0-9]+.[0-9]+)</span>[^N]+NEGATIVE\">([^<]+)',ebaydl, MULTILINE)                                     

        global db_entry                                                                         # initialise the database entry array as global within the function
        
        if item_select.get() == 1:                                                              # if the latest item from ebay is selected then:

            item = ebayitems[0]                                                                 # assigning first item from regex so it can be sliced and displayed
            desc_box["text"] = item[0]                                                          # displaying title
            price["text"] = item[1]                                                             # displaying price

            update_results("Item from Ebay. \nDescription: "+item[2]+"\nURL: "+\
                "https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719")                     # use the update_results function to update the text box to show the description
            
            db_entry = ['Ebay',item[0],item[1]]                                                 # assigning the used data to the database entry array to be used later
            
        elif item_select.get() == 2:                                                            # if the second item from ebay is selected then:

            item = ebayitems[1]                                                                 # assigning second item from regex so it can be sliced and displayed
            desc_box["text"] = item[0]                                                          # displaying title
            price["text"] = item[1]                                                             # displaying price

            update_results("Item from Ebay. \nDescription: "+item[2]+"\nURL: "+\
                "https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719")                     # use the update_results function to update the text box to show the description

            db_entry = ['Ebay',item[0],item[1]]                                                 # assigning the used data to the database entry array to be used later

        elif item_select.get() == 3:                                                            # if the third item from ebay is selected then:

            item = ebayitems[2]                                                                 # assigning third item from regex so it can be sliced and displayed
            desc_box["text"] = item[0]                                                          # displaying title
            price["text"] = item[1]                                                             # displaying price

            update_results("Item from Ebay. \nDescription: "+item[2]+"\nURL: "+\
                "https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719")                     # use the update_results function to update the text box to show the description

            db_entry = ['Ebay',item[0],item[1]]                                                 # assigning the used data to the database entry array to be used later

    except TypeError:                                                                           # if a TypeError is raised the default error text is displayed on the GUI
        print("Type Error")
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Ebay. \nURL: https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719") 

    except IndexError:                                                                          # if an IndexError is raised the default error text is displayed on the GUI                                 
        print("Index Error")
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Ebay. \nURL: https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719")  
        
    except:                                                                                     # any other errors raise the default error text as well
        print('other')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Ebay. \nURL: https://www.ebay.com.au/b/3D-Printers/183063/bn_55158719") 


# function to display buy search sell information
def bss():

    # error trapping is implemented here
    # try the following if there are no errors raised
    try:
        
        # download the bss url using inbuilt function
        bssdl = download("https://www.buysearchsell.com.au/all-locations/pets/?sort=date", incognito=True)      

        # regex to find the title, cost and description from the source code
        bssitems = findall(r"<h2 class=\"listing-header\">[\n ]+([^<]+)<\/h2>[^>]+[>]([AU \$0-9.]+)<\/h3>[^0-9]+[^<]+<div class=\"max-height-static\">[^>]+>([A-Za-z ,.;0-9&-]+)",bssdl)
    
        global db_entry                                                                         # initialise the database entry array as global within the function

        if item_select.get() == 4:                                                              # if the latest item from bss is selected then:

            item = bssitems[0]                                                                  # assigning the first item from the regex to a variable that can be manipulated

            title = str(item[0])                                                                # setting the title to be a string to be manipulated
            title = title.strip(' \n')                                                          # stripping all the spaces and newlines surrounding the text
            titleregexone = findall("([^&#;]+)",title)                                          # using regex to remove the unicode characters
            titleregextwo = findall("[^0-9]+",str(titleregexone))                               # using regex to remove the numbers that were in the unicode
            titlerregexthree = ''.join(titleregextwo)                                           # the above regex splits the string into strings of individual letters, so they need to be joined together
            titlerregexfour = titlerregexthree.strip(",[]'")                                    # stripping the brackets and commas from around the text
            titlerregexfive= findall("[^\"\',]",str(titlerregexfour))                           # using regex to remove the extra quotation marks
            titlerregexfive = ''.join(titlerregexfive)                                          # join the string together
            desc_box["text"] = titlerregexfive                                                  # displaying the title

            if '$' in item[1]:                                                                  # some of the prices displayed on the web page do not feature $,
                cost = item[1]                                                                  # so for ease of use, this if statement adds the $
                price["text"] = cost
            else:
                cost = '$'+item[1]
                price["text"]  = cost

            update_results('Item from Buy Search Sell. \nDESCRIPTION: '+item[2]+\
                '\nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date')        # use the update_results function to update the text box to show the description
            
            db_entry = ['Buy Search Sell',titlerregexfive,cost]                                 # assigning the used data to the database entry array to be used later

        elif item_select.get() == 5:                                                            # if the second item from bss is selected then:

            item = bssitems[1]                                                                  # assigning the second item from the regex to a variable that can be manipulated

            title = str(item[0])                                                                # setting the title to be a string to be manipulated
            title = title.strip(' \n')                                                          # stripping all the spaces and newlines surrounding the text
            titleregexone = findall("([^&#;]+)",title)                                          # using regex to remove the unicode characters
            titleregextwo = findall("[^0-9]+",str(titleregexone))                               # using regex to remove the numbers that were in the unicode
            titlerregexthree = ''.join(titleregextwo)                                           # the above regex splits the string into strings of individual letters, so they need to be joined together
            titlerregexfour = titlerregexthree.strip(",[]'")                                    # stripping the brackets and commas from around the text
            titlerregexfive= findall("[^\"\',]",str(titlerregexfour))                           # using regex to remove the extra quotation marks
            titlerregexfive = ''.join(titlerregexfive)                                          # join the string together
            desc_box["text"] = titlerregexfive                                                  # displaying the title

            if '$' in item[1]:                                                                  # some of the prices displayed on the web page do not feature $,
                cost = item[1]                                                                  # so for ease of use, this if statement adds the $
                price["text"] = cost
            else:
                cost = '$'+item[1]
                price["text"]  = cost

            update_results('Item from Buy Search Sell. \nDESCRIPTION: '+item[2]+\
                '\nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date')        # use the update_results function to update the text box to show the description
            
            db_entry = ['Buy Search Sell',titlerregexfive,cost]

        elif item_select.get() == 6:                                                            # if the third item from bss is selected then:

            item = bssitems[2]                                                                  # assigning the third item from the regex to a variable that can be manipulated

            title = str(item[0])                                                                # setting the title to be a string to be manipulated
            title = title.strip(' \n')                                                          # stripping all the spaces and newlines surrounding the text
            titleregexone = findall("([^&#;]+)",title)                                          # using regex to remove the unicode characters
            titleregextwo = findall("[^0-9]+",str(titleregexone))                               # using regex to remove the numbers that were in the unicode
            titlerregexthree = ''.join(titleregextwo)                                           # the above regex splits the string into strings of individual letters, so they need to be joined together
            titlerregexfour = titlerregexthree.strip(",[]'")                                    # stripping the brackets and commas from around the text
            titlerregexfive= findall("[^\"\',]",str(titlerregexfour))                           # using regex to remove the extra quotation marks
            titlerregexfive = ''.join(titlerregexfive)                                          # join the string together
            desc_box["text"] = titlerregexfive                                                  # displaying the title

            if '$' in item[1]:                                                                  # some of the prices displayed on the web page do not feature $,
                cost = item[1]                                                                  # so for ease of use, this if statement adds the $
                price["text"] = cost
            else:
                cost = '$'+item[1]
                price["text"]  = cost

            update_results('Item from Buy Search Sell. \nDESCRIPTION: '+item[2]+\
                '\nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date')        # use the update_results function to update the text box to show the description
            
            db_entry = ['Buy Search Sell',titlerregexfive,cost]
            
    except TypeError:                                                                           # if a TypeError is raised the default error text is displayed on the GUI
        print('type')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Buy Search Sell. \nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date")

    except IndexError:                                                                          # if an IndexError is raised the default error text is displayed on the GUI
        print('index')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Buy Search Sell. \nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date")

    except:                                                                                     # any other errors raise the default error text as well
        print('else')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Buy Search Sell. \nURL: https://www.buysearchsell.com.au/all-locations/pets/?sort=date")


# function to display japan today information
def japan():

    # error trapping is implemented here
    # try the following if there are no errors raised
    try:

        # download the japan today using the inbuilt function
        japdl = download("https://classifieds.japantoday.com/index/index/category/appliance", incognito=True)   
        
        # regex to find the title and cost from the source code
        japitems = findall('category\/appliance\/article_id\/[0-9]+">([^J<]+)([(JPY 0-9\n,]+)', japdl, MULTILINE)                                                            

        japdesc = findall('post_date">[^\/]+\/div>[^>]+>([^<]+)',japdl, MULTILINE)              # regex to find the description from the source code

        global db_entry                                                                         # initialise the database entry array as global within the function

        if item_select.get() == 7:                                                              # if the latest item from japan today is selected then:

            item_one = str(japitems[0]).split(',')                                              # assigning and splitting the first item of the regex to be the latest item

            title = item_one[0]                                                                 # setting the title to be the first item                                                                 
            title = title[2:-1]                                                                 # slicing the string to remove the extra characters
            title = title.strip('(')                                                            # stripping the brackets from the string

            cost = str(item_one[1:])                                                            # slicing and converting the second item into a string for the cost
            cost = findall('([A-Z,0-9]+)',cost)                                                 # find all the letters and numbers from the cost string
            cost = ''.join(cost)                                                                # join the cost back together

            desc = str(japdesc[0]).strip(' \n\r')                                               # convert the description to a string and strip all new lines and spaces

            if cost:                                                                            # some of the prices displayed on the web page aren't displayed, so for ease of use
                displaycost = cost                                                              # this if statement tests to see if there is a price listed, and if there is not
                price["text"] = displaycost                                                     # it displays the text 'not listed on main page'
            else:
                displaycost = "Not listed on Main Page"
                price["text"] = displaycost

            desc_box["text"] = title                                                            # displaying the title

            update_results("Item from Japan Today. \nDESC: "+desc+\
                "\nURL: https://classifieds.japantoday.com/index/index/category/appliance")     # using the update_results function to update the text box to show the description

            db_entry = ['Japan Today',title, displaycost]                                       # assigning the used data to the database entry array to be used later

        elif item_select.get() == 8:                                                            # if the second item from japan today is selected then:

            item_two = str(japitems[2]).split(',')                                              # assigning and splitting the third item of the regex to be the second latest item
                                                                                                # the regex captures the same string every second item, so the code has adjusted for this

            title = item_two[0]                                                                 # setting the title to be the first item                                                                 
            title = title[2:-1]                                                                 # slicing the string to remove the extra characters
            title = title.strip('(')                                                            # stripping the brackets from the string

            cost = str(item_two[1:])                                                            # slicing and converting the second item into a string for the cost
            cost = findall('([A-Z,0-9]+)',cost)                                                 # find all the letters and numbers from the cost string
            cost = ''.join(cost)                                                                # join the cost back together

            desc = str(japdesc[0]).strip(' \n\r')                                               # convert the description to a string and strip all new lines and spaces

            if cost:                                                                            # some of the prices displayed on the web page aren't displayed, so for ease of use
                displaycost = cost                                                              # this if statement tests to see if there is a price listed, and if there is not
                price["text"] = displaycost                                                     # it displays the text 'not listed on main page'
            else:
                displaycost = "Not listed on Main Page"
                price["text"] = displaycost

            desc_box["text"] = title                                                            # displaying the title

            update_results("Item from Japan Today. \nDESC: "+desc+\
                "\nURL: https://classifieds.japantoday.com/index/index/category/appliance")     # using the update_results function to update the text box to show the description

            db_entry = ['Japan Today',title, displaycost]                                       # assigning the used data to the database entry array to be used later

        elif item_select.get() == 9:                                                            # if the third item from japan today is selected then:

            item_three = str(japitems[4]).split(',')                                            # assigning and splitting the fifth item of the regex to be the latest item

            title = item_three[0]                                                               # setting the title to be the first item                                                                 
            title = title[2:-1]                                                                 # slicing the string to remove the extra characters
            title = title.strip('(')                                                            # stripping the brackets from the string

            cost = str(item_three[1:])                                                          # slicing and converting the second item into a string for the cost
            cost = findall('([A-Z,0-9]+)',cost)                                                 # find all the letters and numbers from the cost string
            cost = ''.join(cost)                                                                # join the cost back together

            desc = str(japdesc[0]).strip(' \n\r')                                               # convert the description to a string and strip all new lines and spaces

            if cost:                                                                            # some of the prices displayed on the web page aren't displayed, so for ease of use
                displaycost = cost                                                              # this if statement tests to see if there is a price listed, and if there is not
                price["text"] = displaycost                                                     # it displays the text 'not listed on main page'
            else:
                displaycost = "Not listed on Main Page"
                price["text"] = displaycost

            desc_box["text"] = title                                                            # displaying the title

            update_results("Item from Japan Today. \nDESC: "+desc+\
                "\nURL: https://classifieds.japantoday.com/index/index/category/appliance")     # using the update_results function to update the text box to show the description

            db_entry = ['Japan Today',title, displaycost]                                       # assigning the used data to the database entry array to be used later

    except TypeError:                                                                           # if a TypeError is raised the default error text is displayed on the GUI
        print('type')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Japan Today. URL: https://classifieds.japantoday.com/index/index/category/appliance")

    except IndexError:                                                                          # if an IndexError is raised the default error text is displayed on the GUI
        print('index')
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Japan Today. URL: https://classifieds.japantoday.com/index/index/category/appliance")

    except:                                                                                     # any other errors raise the default error text as well
        desc_box["text"] = 'No item description available'
        price["text"] = '-- $--.--'
        update_results("Item from Japan Today. URL: https://classifieds.japantoday.com/index/index/category/appliance")

# function to update the textbox which displays the description of the item
def update_results(description):
    source.delete(0.0, END)                                                                     # deletes previous entry 
    source.insert(END, description)                                                             # adds new entry

# function to enter into the selected data into the database
def database():

    connection = connect(database='classifieds.db')                                             # create a connection to the database
    classifieds_db = connection.cursor()                                                        # create a cursor
    classifieds_db.execute("DELETE FROM current_selection")                                     # execute the query to delete all items from the database

    source = db_entry[0]                                                                        # assigning the source to be the first item from the list
    description = db_entry[1]                                                                   # assigning the description to be the second item from the list
    price = db_entry[2]                                                                         # assigning the price to be the third item from the list

    classifieds_db.execute("INSERT INTO current_selection VALUES ('"+source+"', \
        '"+description+"', '"+price+"')")                                                       # execute the query to insert the source, description and price into the database

    connection.commit()                                                                         # commit the data to the connection

    classifieds_db.close()                                                                      # close the database

    connection.close()                                                                          # close the connection

    from tkinter import messagebox                                                              # import the messagebox into the function
    messagebox.showinfo('Save', 'Item has been saved')                                          # show a messagebox to say that the item has been saved to the database


#-------<VARIABLES>-------#

#<dimensions>
length_grid = 10
height_grid = 10

#<colours>
main = '#12182E'
accent = '#5CE1E6'
accent2 = '#9AECF0'

#<fonts>
font = ('Century Gothic',14,'bold')
font2 = ('Century Gothic',10)
font3 = ('Century Gothic',8)
font4 = ('Century Gothic',8,'bold')
font5 = ('Century Gothic',6)


#--------MAKING WIDGETS-------#

#< making the main window>
ad_window = Tk()
ad_window.title('Classified Ads')
# <styling the window>
ad_window.geometry('575x700')       # setting size of window
ad_window["bg"] = main              # setting background colour

#<variables>
shop_selection = IntVar()           # the variable assigned to each shop
item_select = IntVar()              # the variable assigned to each of the item options in the shops, ranging from 1-9 for each option, so that only one can be selected at one time
savestate = IntVar()                # the variable assigned to the save button

#<header widgets>

# empty label widget for spacing
placement_block = Label(ad_window,background='#12182E',width=int(length_grid*0.3))                                     

# frame for title image  
title = Frame(ad_window,borderwidth=10,relief="ridge",background=accent)  

# image canvas for title image
little = Canvas(title,height=40,width=300,background=accent2,relief='groove')                                                  

# importing title image   
icon = PhotoImage(file='header.png')                                 


# <Option One Widgets> - 3D Printers from Ebay

# Logo and Shop Selection
# frame for all option one components
option_one = Frame(ad_window, width = int(length_grid*1.5),height = int(height_grid*1.15),borderwidth=5,relief="ridge")            
# option one text
first_label = Radiobutton(option_one,text='3D Printers', font=font, foreground=main, variable=shop_selection, value=1,cursor="hand2")       
# creating canvas for ebay image
image_one = Canvas(option_one,height=70,width=140)                          
# importing ebay image
ebay_photo = PhotoImage(file='ebat.png')                                    

# Selection Choices
# making frame to store the ebay options 
choices_one = Frame(option_one, height = 3, width = 4,borderwidth=3,background=accent2,relief='groove')
# option one: latest item - variable 1                                     
choices_11 = Radiobutton(choices_one, text = 'Latest Item', width=10,borderwidth=3, variable=item_select,value=1, command=ebay,justify=CENTER,background=accent2,cursor="hand2")                   
# option two: second latest item - variable 2
choices_12 = Radiobutton(choices_one, width=10,text = 'Second Item',borderwidth=3,variable=item_select,value=2, command=ebay,justify=CENTER,background=accent2,cursor="hand2")
# option three: third latest item - variable 3
choices_13 = Radiobutton(choices_one, width=10,text = 'Third Item', borderwidth=3,variable=item_select,value=3, command=ebay,justify=CENTER,background=accent2,cursor="hand2")



# <Option Two Widgets> - Pets from Buy Search Sell

# Logo and Shop Selection
# frame for all option two components
option_two = Frame(ad_window, width = int(length_grid*1.5),height = int(height_grid*1.15),borderwidth=5,relief="ridge")    
# option two text
second_label = Radiobutton(option_two,text='Pets',variable=shop_selection, value = 2, font=font,foreground=main,cursor="hand2")                           
# creating canvas for amazon image
image_two = Canvas(option_two,height=70,width=140)                  
# importing amazon image    
bss_photo = PhotoImage(file='bss_photo.png')  

# Selection Choices
# making a frame to store the bss options
choices_two = Frame(option_two, height = 3, width = 4,borderwidth=3,background=accent2,relief='groove')
# option one: latest item - variable 4
choices_21 = Radiobutton(choices_two, text = 'Latest Item', width=10,borderwidth=3, variable=item_select,value=4, command=bss,justify=CENTER,background=accent2,cursor="hand2")
# option two: second latest item - variable 5
choices_22 = Radiobutton(choices_two, width=10,text = 'Second Item',borderwidth=3,variable=item_select,value=5, command=bss,justify=CENTER,background=accent2,cursor="hand2")
# option three: third latest item - variable 6
choices_23 = Radiobutton(choices_two, width=10,text = 'Third Item', borderwidth=3,variable=item_select,value=6, command=bss,justify=CENTER,background=accent2,cursor="hand2")



# <Option Two Widgets> - Pets from Buy Search Sell

# Logo and Shop Selection
# frame for all option three components
option_three = Frame(ad_window, width = int(length_grid*1.5),height = int(height_grid*1.15),borderwidth=5,relief="ridge")
#option three text
third_label = Radiobutton(option_three,text='Appliances',variable=shop_selection, value = 3,font=font,foreground=main,cursor="hand2")                                      
#creating canvas for japan image
image_three = Canvas(option_three,height=70,width=140)              
#importing japan image
japan_photo = PhotoImage(file='japan.png')   

# Selection Choices
# making a frame to store the japan options
choices_three = Frame(option_three, height = 3, width = 4,borderwidth=3,background=accent2,relief='groove')
# option one: latest item - variable 7
choices_31 = Radiobutton(choices_three, text = 'Latest Item', width=10,borderwidth=3, variable=item_select,value=7, command=japan,justify=CENTER,background=accent2,cursor="hand2")
# option two: second latest item - variable 8   
choices_32 = Radiobutton(choices_three, width=10,text = 'Second Item',borderwidth=3,variable=item_select,value=8, command=japan,justify=CENTER,background=accent2,cursor="hand2")
# option three: third latest item - variable 9
choices_33 = Radiobutton(choices_three, width=10,text = 'Third Item', borderwidth=3,variable=item_select,value=9, command=japan,justify=CENTER,background=accent2,cursor="hand2")


# <Show and Save Widgets>
# creating a frame for the two buttons
so_box = Frame(ad_window,width=15*length_grid,height=8*height_grid,background=accent,borderwidth=5,relief='ridge')                     
# show options button
show_options = Checkbutton(so_box, text = 'SHOW DETAILS',indicatoron=False,activeforeground=accent, font=font2,border=3,relief='raised',foreground=main,activebackground=main, command=showurl,cursor="hand2") 
# save button
save = Checkbutton(so_box, text= 'SAVE',indicatoron=False,activeforeground=accent, font=font2,border=3,relief='raised',foreground=main,activebackground=main, variable=savestate,command=database,cursor="hand2")          


# <Description Box Widgets>
# creating a frame for all the labels
description = Frame(ad_window,width=length_grid,height=int(height_grid),borderwidth=5,relief='ridge')                    
# label for putting the items' description
desc_box = Label(description,text = 'SELECTION DESCRIPTION',font=font4,background=accent2,border=3,relief='groove',width=length_grid*3,height=int(height_grid*0.5),wraplength=150)             
# label for putting the items' price
price=Label(description,text='$00.00',font=font3,background=accent2,border=3,relief='groove',height=int(height_grid*0.5),width=length_grid,wraplength=50)                  
# frame for the description
sourceframe = Frame(description,height=int(height_grid/1.5),width=length_grid*5)
# creating a scrollbar for the description box
scrollbar = Scrollbar(sourceframe, orient='vertical')
# textbook for the information to go into
source=Text(sourceframe,font=font3,bg=accent2,borderwidth=3,relief='groove',height=int(height_grid/1.5),width=length_grid*5,yscrollcommand = scrollbar.set)
# inserting default text
source.insert(END, "Source and URL")


#--------PLACING WIDGETS-------#
# using grid()

# <placing header elements>

placement_block.grid(row=1,column=1)                                    # placing placement block in the first column                   
title.grid(row=1, column=2, columnspan=5,pady=height_grid)              # placing title frame across the top
little.grid(row=1,column=1,sticky='we')                                 # placing image canvas in frame
little.create_image(160,20,image=icon)                                  # placing image in canvas


# <placing option one elements>

option_one.grid(row = 2,column=2,padx=5,pady=10)                        # placing option one frame
image_one.grid(row=1,column=1)                                          # placing image canvas in frame
image_one.create_image(70,40,image=ebay_photo)                          # placing image in canvas
first_label.grid(row=2,column=1,sticky='we')                            # placing label below image
choices_one.grid(row = 3,column=1, ipadx=20,padx=5,pady=20)             # placing list below label
choices_11.grid(row=1)                                                  # placing choice one (latest)
choices_12.grid(row=2)                                                  # placing choice two (second)
choices_13.grid(row=3)                                                  # placing choice three (third)


# <placing option two elements>

option_two.grid(row = 2,column=3,padx=5,pady=10)                        # placing option two frame
image_two.grid(row=1,column=1)                                          # placing image canvas in frame
second_label.grid(row=2,column=1)                                       # placing image in canvas
image_two.create_image(70,40,image=bss_photo)                           # placing label below image
choices_two.grid(row = 3,column=1, ipadx=20,padx=5,pady=20,sticky='S')  # placing list below label
choices_21.grid(row=1)                                                  # placing choice one (latest)
choices_22.grid(row=2)                                                  # placing choice two (second)
choices_23.grid(row=3)                                                  # placing choice three (third)


#<placing option three elements>

option_three.grid(row = 2,column=4,padx=5,pady=10)                      # placing option three frame
image_three.grid(row=1,column=1)                                        # placing image canvas in frame
third_label.grid(row=2,column=1)                                        # placing image in canvas
image_three.create_image(70,40,image=japan_photo)                       # placing label below image
choices_three.grid(row=3,column=1,ipadx=20,padx=5,pady=20,sticky='S')   # placing list below label
choices_31.grid(row=1)                                                  # placing choice one (latest)
choices_32.grid(row=2)                                                  # placing choice two (second)
choices_33.grid(row=3)                                                  # placing choice three (third)


# <placing save and show elements>

so_box.grid(row=4,column=2,columnspan=3,pady=5)                         # placing save and show frame
show_options.grid(row=1,column=1,padx=20,pady=5)                        # placing show button
save.grid(row=1,column=2,padx=20,pady=5)                                # placing save button


#<placing description elements>

description.grid(row=6,column=2,columnspan=5,padx=5,pady=10,rowspan=2)  # placing description frame
desc_box.grid(row=1,column=1,padx=10,pady=5)                            # placing description label
price.grid(row=1,column=2,pady=5,padx=5)                                # placing price label
sourceframe.grid(row=2,column=1,pady=5,padx=20,columnspan=2)            # placing source frame
source.grid(row=0,column=0)                                             # placing source text box
scrollbar.grid(row=0,column=1,sticky='ns')                              # placing scroll bar
scrollbar.config(command=source.yview)                                  # connecting the scroll bar and text box


#-----Generating Window------#

ad_window.mainloop()
