For any modification take a look at the signe : /C/

This might be some html balise or code.


Here is an accurate scrapper in slightly draft recovery in the storage of data that see itself retained in different types of variable.

This Scraper is easy to use:

The Phi-Gestionner file is there to launch the program.

The Init_BDD.py file is the origin of everything
If the site link changes, you must modify the "link" variable in the StartBrowser() function:
What you need to know about this class is that it uses the site for the first time and sends one by one the links of the calls to be scrapped to the file described below.

The parsing.py file is when has it to retrieve the data on a web page accurately and send the information in a database.
If the site changes you can keep the data sent. But in this case I advise you to keep just the Init(self,url,ft_ddb) function.
Thus you will be able to choose a single type of variable, a number of table in the database as you wish, and finally of course a whole new parser.

This class is simple you can inbstanciez it and call the function Init which takes in parameter, an url and return the function MySQLdb.connect()