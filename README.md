## <ins>About this project</ins>
This project aims to practice some of the things I have been learning lately about Machine Learning, and being able to integrate those into more complex Django app. 
During this project, I have acquired and practiced various important skills including:
<ul>
    <li>Some exploratory data analysis using plots.</li>
    <li>Model selection and hyperparameter tuning using grid search with cross validation.</li>
    <li>Predictive system using train test split.</li>
    <li>Using the model in a Django app using pickle files.</li>
    <li>Web scraping to get dollar and euro values from another website.</li>
    <li>Django form based on a Django model.</li>
    <li>File input in Django.</li>
    <li>CRUD operations in Django.</li>
    <li>Present the data in charts in the Django app using Chart.js.</li>
</ul>

## <ins>About the problem</ins>
Term deposits are a major source of income for a bank. A term deposit is a cash investment held at a financial institution. Your money is invested for an agreed rate of interest over a fixed amount of time, or term. The bank has various outreach plans to sell term deposits to their customers such as email marketing, advertisements, telephonic marketing, and digital marketing.

Telephonic marketing campaigns still remain one of the most effective way to reach out to people. However, they require huge investment as large call centers are hired to actually execute these campaigns. Hence, it is crucial to identify the customers most likely to convert beforehand so that they can be specifically targeted via call.

The data is related to direct marketing campaigns (phone calls) of a Portuguese banking institution. The classification goal is to predict if the client will subscribe to a term deposit.



## <ins>To run Django project</ins>

### <ins>Commands on terminal</ins>
\$ virtualenv venv <br>
\$ pip install -r requirements.txt <br>
\$ . venv/Scripts/activate <br> 
\$ python manage.py runserver 


## <ins>To run Jupyter notebook</ins>
### <ins>Commands on terminal</ins>
\$ virtualenv venv <br>
\$ pip install -r requirements.txt <br>
\$ . venv/Scripts/activate <br>
\$ jupyter notebook 

**Note that if you installed the requirements to run the Django project, you don't need to install them again for the Jupyter Notebook and vice versa.**

**You will also need to create a .env file in the root folder with the following variables:**


SECRET_KEY=<i>Your secret key</i><br>
DB_USER=<i>Your user (usually root)</i><br>
DB_PASSWORD=<i>Your password</i><br>
DB_HOST=<i>Your host (usually localhost)</i><br>
DB_PORT=<i>Your port (usually 3306 for MySQL)</i><br>
DB_NAME=<i>Your database name</i><br>

You can also just modify this information on settings.py file in CapitalCall folder.



