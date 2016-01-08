Obejctive: 
 

The objective of this software is to implement a Swiss-system tournament. The user needs to install a virtual machine as we need to execute this on Linux OS and shell on the virtual machine to invoke the python program. 


Instructions about the contents 

This package contains 4 files 
	2 python files(tournament.py & test.py)
	Tournament.SQL- Please dont use this file (SQL code is included in tournament.py file)
	Readme file  

tournament.py: This python program is the foundation program for this package where the tables are created , deleted, dropped, records are created updated and all database operations are done.

This program has logic to 
Connect to database
to do all database operations (as mentioned above)
has the logic for checking byes (in case of odd number of players)
has logic for validation of avoading duplicate players, duplication of games
has logic to arrive at swiss system of pairing
report player standing and outcomes after matches


Test.py- This is the python file that is for testing tournament.py. This has test data sets to test all the procedures in the tournament file.


Instructions to run test.py
 
1)Please open a virtual machine (you can use vagrant and oracle virutal machine for VM)and access the shell of virtual machine (any bash editor)
2)Navigate to the folder where all the file test.py and tournament.py are stored
3)There is no need to use python.sql, it is included in the package more for completeness of package.
4)Please note test.py will call procedures to drop and create tables from with in python code. The drop tables will only work if tables exist.
5)Execute test.py , this has all test data built in to check all fucntions of the tournament code.
6)After testing all the procedures it will display a message - "testpairings- Tested successfully Success!  All tests pass!"
7)After executing test.py if we get this message it means the program is working successfully.
 