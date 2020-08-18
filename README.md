<a href="http://www.eniso.rnu.tn/fr/"><img align="left" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Logo_ENISo%2C_Tunisie.svg/450px-Logo_ENISo%2C_Tunisie.svg.png" width="120px"></a>
<a href="http://www.intelligencia-it.com/"><img align="right" src="http://www.intelligencia-it.com/images/INTG/Logos/INTG_Small.png" width="200px"></a>
---
# Graduation Project
---
---
>This Repository contains:
- #### Angular frontend interface
- #### Django Backend web Rest API
- #### The project report and the graduation slideshow

---
### Getting Started

> To run this project you should follow these steps.

#### 1) Clone & Install Dependencies
> It is recommended to create a Virtual environment for the Django(python) part
- 1.1) `git clone https://github.com/HaddajiBilel/csv_to_RestAPI.git`
- 1.2) `cd csvToRest` - cd into the Django Rest API.
- 1.3) `pip install -r requirements.txt` - install the project dependencies 
- 1.4) `python manage.py runserver` - run the Backend Rest API 
> The server starts at http://127.0.0.1:8000/ - all the endpoints are mentioned in the Graduation report.
> To test the API endpoints you can use [`postman`](https://www.postman.com/) 

---
> set up the front end user interface
- 1.1) Go to angular/RoboTrading folder 
- 1.2) `npm install` - install all the angular project dependencies.
- 1.3) `ng runserver` - run the angular dashboard
> The frontend server starts at http://localhost:4200/
> Please note that due to cross headers problem ( running 2 servers locally ) you need to add an [`extention`](https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc?hl=en) to the web chrome web browser 
