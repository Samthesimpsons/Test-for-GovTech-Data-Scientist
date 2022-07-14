# GDS-ACE-Tech-Assessment
GDS ACE Tech Assessment TAP 2023

## Details
**Project Title:** 

We are the Champions Web Application

**Description:** 

Build an application to help the event organisers keep track of results for the first round of the championship and determine the current team rankings within each group. More details in the Assessment document.

1. For bonus requirements, entered data is by default hosted on a `SQLite` database. A `MySQL` database hosted by AWS RDS has also been set up as another option. Note, as good practice, my password has been removed from `setAWSPassword.R`.

2. The evaluation of the rankings given the text inputs are handled by `helper.py`. Run the `helper.py` file to test. Only requirement is the `pandas` package, therefore there is no `requirements.txt` file for venv setup.

3. For the backend and front-end services, my initial plan was to use `FastAPI` and `vue.js`. However, I am not an expert in those fields, hence I chose `RShiny` in `R`, which handles both front-end and server side.  Nevertheless, my previous progress is still uploaded under `initial` folder. For `python` and `R` integration, we will be using the `reticulate` package.

4. For bonus requirements, the text inputs have a check validity button before allowing for scoring which will display either a successful or wrong input. Note that our queries to the database is posting pushing and pulling an entire dataframe, none of the text inputs are directly used in any queries. Hence, `SQL injection` handling is not done.

4. For bonus requirements, the web application and the SQLite database is hosted onto `shinyapps.io` free server.

**Requirements:**
1. Python 
2. R
3. RStudio (preferred IDE for R programming)

**How to run:**

Open up RStudio and load the `app.R` file. As a new R user, simple uncomment the first few lines, which is a custom package handler to download all the necessary packages. 

Then all you need to do is ensure under `.Rprofile`, the python path is set to the python path of your local machine.

Finally, just click `run App` option on the top right, to run the web application locally.

If not, simple check the publicly hosted web application:
https://samuelsim.shinyapps.io/TAPapplication/
