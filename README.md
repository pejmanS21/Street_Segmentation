# Street_Segmentation

## Colab

run provided notebook in google colab:

<a href="https://colab.research.google.com/drive/1PvP-g-NI11ld5oDCKEK13lodv1iEHvbl?usp=sharing" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

<br>

## About

A segmenter on street view with 23 class, for self driving car. from this [link](https://www.kaggle.com/kumaresanmanickavelu/lyft-udacity-challenge) you can check dataset on kaggle. <br>
Images are in shape (160, 240) and 3 channels, Model is UNet in Pytorch framework.
<br>

## Usage 

first download unet model from google drive by execute [get_weights.sh](./models/get_weights.sh):

    chmod +x get_weights.sh
    ./get_weights.sh

then in your local computer to start `Django` server run following commands in your terminal:

1- **makemigrations**

    $ python3 manage.py makemigrations

2- **migrate**

    $ python3 manage.py migrate

3- **runserver**

    $ python manage.py runserver 0.0.0.0:8000

<br>

>***Note***: don't forget to install requirements.txt

    $ pip3 install -r requirements.txt

<br>

## Docker

    $ docker-compose up --build

<br>

## UI

![mainpage](./media/ui_1.png)

![dispaly](./media/ui_2.png)