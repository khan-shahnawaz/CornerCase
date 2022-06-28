# CornerCase

A web application designed to find the corner test cases for incorrect code built using django, redis and celery. The site is deployed [<ins> here </ins>](http://www.cornercase.cf/)


## Installation

The application has been dockerised and no dependencies has to be installed apart from docker.

Docker can be installed from [<ins> here </ins>](https://docs.docker.com/desktop/)


## Run Commands

Clone the repository by the command 
```
git clone https://github.com/skhan-org/CornerCase
```

Ensure that you are in the project directory containing manage.py and run the following commands:
```
docker-compose build
docker-compose up
```

This will start the server at [<ins>http://127.0.0.1:8000/</ins>](http://127.0.0.1:8000/)


## Usage

The application can find a randomly generated testcase at which your program fails. For that follow these steps:

* Make a test generator in any programming language supported by the application. It is recommended to keep the tests small to get better idea about the failing case. More about generators [<ins> here </ins>](https://www.geeksforgeeks.org/test-case-generation-set-1-random-numbers-arrays-and-matrices/)
* In the homepage of the application, put your code,  editorial's code and generator code and select appropriate programming language in the text box mentioned. Click on submit.

![127 0 0 1_8000_ (10)](https://user-images.githubusercontent.com/79746977/174814530-eb8c06a5-fa02-4c27-bf54-db93fba71e56.png)


* The application will show the failing testcase if it is found within 10 trials. If not found, then start the process again to test your code on more testcases.

![127 0 0 1_8000_status_9](https://user-images.githubusercontent.com/79746977/174815030-c5b30b84-28ff-4f0c-95f4-d78617ab3b7f.png)


## Admin Panel

The admin panel can be accessed through the url [<ins>http://127.0.0.1:8000/admin</ins>](http://127.0.0.1:8000/admin)

In the database provided with the repository, the admin credentials are as follows:
```
Username: admin
E-mail: admin@admin.com
Password: admin
```
Note: *The admin username and password can be changed by logging into the admin panel*

New superuser can be added by the following commands in the base directory of the project:

```
python manage.py createsuperuser
```

Note: *For executing the above instructions, django and python 3 should be installed in the host machine*

Alternatively, admin panel can be used to add superusers

The admin portal shows the following details:

* **Executable**: It consists of the codes submitted in the portal with their programming language. The form submission time is also recorded. The testcases generated are also shown along with its position in the queue.

![127 0 0 1_8000_admin_Tester_executable_](https://user-images.githubusercontent.com/79746977/174819174-93b07fe7-ff80-4428-bc6d-0f3df3e31e14.png)
<br/>
<br/>

![127 0 0 1_8000_admin_Tester_executable_9_change_](https://user-images.githubusercontent.com/79746977/174819360-1fe43b70-2479-4ba9-a683-5646691569c0.png)

* **Testcase**: The testcase generated is shown along with the output received from the user and the editoral's code. It also shows which executable it belongs

![127 0 0 1_8000_admin_Tester_test_22_change_](https://user-images.githubusercontent.com/79746977/174819904-75ad1640-731d-4fb8-a27f-cbfa57726d4a.png)


* **Programming Language**: In the default database file provided in the repository, python 3.7 and C++ is 17 is added. More programming language can be added through the admin panel. To do so, follow these steps:

  * Click on Programming Language in the sidebar then click on Add programming Language.
  * Enter name, compile command, execution command and extension of the programming language.
  * Enter the name of the docker image on which the programs of that language will run.
  * Make sure that the docker images for each language are pulled in the host system.
    ##### Compile command format
      * Write how to compile the file in the language by writing its command. Eg. g++ filename. The token filename will be replaced by actual code file name at the time of compilation.
      * If the language is not compiled, simply write 'NA' (case-sensitive, without quotes).
   
    ##### Execute command format
      * Write the command to execute the file. For eg. python filename. filename will be replaced by the code file name at the time of executation
      * If the language is compiled, simply write 'NA' (case-sensitive, without quotes).

![ec2-44-207-10-175 compute-1 amazonaws com_8000_admin_Tester_programminglanguage_1_change_](https://user-images.githubusercontent.com/79746977/175820212-4e4905f2-30f3-4446-b2b8-8d6ee4cea1d9.png)

