# Calix

Willow's simple calendar.

I made this because I'm a college student whose life is run through Google
Calendar.
I adore GCal, but it's got more than I need and runs poorly on my crappy laptop.
I just want something simple, fast, and perfectly molded to my specific needs.
Sorry everybody else.

## Requirements

- Python 3.14 (but probably works on older versions)
- Node.js 25 (but probably works on older versions)
- MariaDB 12

## Install (Ubuntu)

The following assumes you are starting from a bare Ubuntu setup.
Skip the parts you don't need to do.

```
sudo apt update

# install python
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.14 python3.14-venv

# install node 25 (using nvm)
sudo apt install curl
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
nvm install 25
nvm use 25

# install a mariadb database (using docker)
# ================== docker install ===================
# Add Docker's official GPG key:
sudo apt install ca-certificates
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# ================ end docker install =================
docker run --detach --name calix-db --env MARIADB_ROOT_PASSWORD=example MARIADB_DATABASE=calix -p 3306:3306 mariadb:latest
```

## Setup (Ubuntu)

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
cd calix
flask db upgrade
cd ../..

cd frontend/calix
npm i
cd ..
```

## Run (Dev)

In one terminal:

```
cd backend/calix
flask run
```

In another:

```
cd frontend/calix
npm run dev
```

Calix will be running on http://localhost:3000.
