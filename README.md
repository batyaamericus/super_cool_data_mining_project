# Comeet Web Scraper!

This project is a web scraper developed to retrieve open data scientist jobs from cloud-based collaborative hiring platform [Comeet](https://www.comeet.com/), with an extension in a form of basic user interface that allows searching for specific information about companies and their available positions based on different parameters. Comeet is an ATS commonly used by Israeli hi-tech companies. Their company pages are available via direct link, but will not show up in a Google search hence we hope this application will facilitate easier use of the platform.


## Code breakdown

Below is a short summary of different parts of the project, which can be run together or on their own, depending on the desired outcome.

### Part 1: Database Creation
Code files:

 - [database.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/database.py)

The code source contains two functions create_db( )  and create_tables( ) that create a schema called comeet_jobs and database tables respectively according to the below ERD:

![](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/database_diagram.png)


### Part 2: Scraping

Code files:

 - [scraper.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/scraper.py)
 - [finding_websites.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/finding_websites.py)
 - [db_details.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/db_details.py)
 
This part first uses google API to get top 100 google search results for pages containing *"data scientist"* on Comeet domain (functions defined in *finding_websites.py*).  It then scrapes the pages for information about open positions per company and populates the database described in previous part using *fill_db_tables()*.

### Part 3: Data Enrichment
Code files:

 - [api_enrichment.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/api_enrichment.py)

This part makes API search calls to [People Data Labs](https://www.peopledatalabs.com/) in order to get more profile information about each of the companies that present in the database and then add it as a new table in the comeet_jobs schema.

### Part 4: User Interface
Code files:

 - [user_interface_menu.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/user_interface_menu.py)
 - [interface_functions.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/interface_functions.py)
 - [new_arg_parser.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/new_arg_parser.py )
 - [db_search_functions.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/db_search_functions.py)

This part, initiated by a call to *main_menu( )* in *user_interface_menu.py* is responsible for running a user interface as an infinite loop until the user chooses to quit the application. The user is given prompts to enter search and display parameters that will be used to retrieve and present data from the database.

### The sequence of parts as it appears in *user_interface_menu.py*:
> database.create_db()  
database.create_tables()  
scraper.scraping()  
scraper.fill_db_tables()
response = api_enrichment.api_enrichment()
api_enrichment.add_info_to_db(response)
main_menu()
## Setup and configuration requirements

 -  This code was written in Python 3.9, so ensure your interpreter's version is no older than that.
 -  To clone this repository to your local directory:
    
    > `git clone https://github.com/batyaamericus/super_cool_data_mining_project.git`
    
 -  Move to the super_cool_data_mining_project directory that you just created.
    
    > `cd super_cool_data_mining_project`
    
 -  Make sure that all of the requirements in the [requirements.txt](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/requirements.txt) are met by your working environment.
 - Go to [config.py](https://github.com/batyaamericus/super_cool_data_mining_project/blob/main/config.py) and change the following lines:
 >user_name = os.environ['username']
 >password = os.environ['password']
 >host = os.environ['host']
 
 such that `os.environ['...']` is the value for the variables you wish to use to access your MySQL database. Similarly, change any of the API keys in the config file as needed.
 Note: you can also declare environment variables when running the script.
 


 -  Run *user_interface_menu.py*! Note that every time you run this file, the program will scrape the internet for new job positions. This will take a few minutes.
    
    > in command line:  `python user_interface_menu.py`
    
	 - You can also choose to run any of the parts of the project separately. Please refer to above summaries and comment out/delete any function you do not wish to call in the *user_interface_menu.py* file
	 - Note: if your operating system does not recognise the  `python`  command, try running  `python3`
