# Pre-Production Email Testing - Instructions & Configuration

## Overview
This project provides an email service designed to act as a plugin module for a broader notification system. Developed in Python, this service is tailored for pre-production testing, ensuring that email notifications are correctly formatted, sent, and received before deployment. The service is dockerized, making it easily integrable and scalable within any application ecosystem requiring email notification capabilities.

## Features
- **Email Template Management**: Create, edit, and manage email templates with dynamic placeholders.
- **Pre-Production Testing**: Test email sending capabilities in a sandbox environment to ensure reliability and correctness.
- **Integration Ready**: Designed as a plug-and-play module for existing notification systems.
- **Customizable Settings**: Configure SMTP settings, email content, and more through a user-friendly interface.

## Notification System
A notification system sends a message to a group of receivers using a combination of hardware and software. 

## Email Infrastructure
- **Email Template Management**
Email User Agents (MUAs): E-mail programs such as Gmail, Outlook, and Thunderbird are included in this. With dynamic placeholders, users can design, modify, and maintain email templates that are tailored to their target audience and appear professional.
  
- **Pre-Production Testing**
Mail Submission Agent (MSA): Serves as a liaison between the Mail Transfer Agent (MTA) and the MUA to guarantee that emails are proofread in a sandbox before being sent. 
Mail Transfer Agent (MTA): Manages the actual email sending process because the system is set up to mimic email delivery without really sending emails, guaranteeing that any potential problems are found and fixed. 
  
- **Integration Ready**
Makes certain that emails are sent and formatted correctly as part of the overall notification workflow.
  
- **Customizable Settings**
SMTP Server Configuration: A user-friendly interface allows users to customize the SMTP parameters. Configuring the SMTP server, authentication methods, and further email delivery settings are all included in this.humiliated in any setting. Docker provides a consistent environment for the email service by making sure that all configurations and dependencies are included.
Authentication Protocols: The assurance of verified emails and increased likelihood of reaching the recipient's inbox is provided via support for SPF, DKIM, and DmARC. These security measures shield the email's content and aid in sender identification verification. 

## Composite Objects Used for the App
- **settings**: Defines kafka broker's address and specifies the topic to subscribe to.
- **smtp_Settings**: Connects to mail trap so that the app is connected to the server and port, thus able to send messages to the environment.
- **emailer**: Puts the files in email_templates together (header, body, footer) and sends it to mail trap to test that the formatting comes out correctly.

## Mailtrap
Mail Trap is an email delivery platform that allows customers to manager the mail infrastructure in on place.

## Docker

## Installation & Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repository/email-service.git
   cd email-service
2. **Create mailtrap account**
3. **Docker compose**
4. **Run python file**

