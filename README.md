# Multi Server Authentication service using Bio-Hash.
### It uses hash values generated using images for validation of user credentials and server authorization by a user.

### 1. Architecture
![Architecture](/static/images/arch.svg "Architecture")

### 2. Deployment
![Deployment](/static/images/deploy.svg "Deployment")
  
### 3. Usecases:- 
- 1. It can be used as <b>Authentication as a Service</b>.

- 2. <b>OpenID Connect</b> can also added to it.

- 3. <b>Scope mechanism</b> of <b>OAuth 2.0</b> can be added in an application's access to a user's account.

### 4. Tech Stack Used:-
- Python3
- Flask (Web Framework)
- SqliteDB
- Pymongo
- PyCryptoDome (AES Enc-Dec)
- <b>bio_auth</b> (Custom Package)
- PyJWT
- Pillow
- ImageHash
- HMAC
- Hashlib
- Pytz

### Setup Application

- Download this git repo.
```
git clone https://github.com/A4ANK/auth_service_biohash.git
```

- Create a virtual env for this app in python.
```
pip install virtualenv

python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
```

- Launch Flask web app.
```
python app.py
```

### Author:-
- Ankur Dhakar