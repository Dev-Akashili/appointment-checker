## Appointment Checker

This is a program built to simulate a browser of and monitor the availability of appointment slots for schengen visa application on the TLS website. It uses Selenium to simulate a Chrome browser environment and uses EmailJS api to send a notification when a slot opens up.

## Getting Started

- `git clone https://github.com/Dev-Akashili/appointment-checker`
- `pip install selenuim` on windows or `pip3 install selenuim` on mac
- `pip install request` on windows or `pip3 install request` on mac
- `python app.py` on windows or `python3 app.py` on mac

You need to make sure you fill in the right URLs for it to work right. You can also change the repo based on the target site to get the desired result.

## Email Notification

To send an email when a slot is available, EmailJs api is used. To set this up you will need to create an account at https://www.emailjs.com/ and get a public key, service Id and create a template.
