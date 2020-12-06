# API

# Installation
+ Run the next command in the current directory `pip install -r requirements.txt`

# Linux daemon
+ Create service file `sudo nano /etc/systemd/system/proyecto-final-sp-api.service`, check `config/proyecto-final-sp-api.service`.
+ Change permissions `sudo chmod 644 /etc/systemd/system/proyecto-final-sp-api.service`
+ Reload os daemons `sudo systemctl daemon-reload`
+ Enable service `sudo systemctl enable proyecto-final-sp-api`
+ Start service `sudo systemctl start proyecto-final-sp-api`
+ Check status `sudo systemctl status proyecto-final-sp-api`

# Database configuration
The url from the database is hardcoded in the `database/db_connection.py` file.
You should change the name of the key where your database would be placed.
Temporaly, it will be using the MongoDB Atlas URL.

# Upload folder
All the files uploaded will be storage in [Cloudinary](cloudinary.com).
Check `config/cloudinary.py`.
