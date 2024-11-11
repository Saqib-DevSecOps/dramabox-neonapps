# Dramabox Application

## Overview

The **Dramabox Application** is a streaming platform designed to provide users with a seamless experience for watching series, including dramas, movies, and TV shows. With features like user management, video streaming, recommendations, payments, notifications, and content reviews, **Dramabox** delivers an intuitive and enjoyable viewing experience.

This cross-platform application will be available on both **Android** and **iOS**, powered by a monolithic backend architecture and integrated with external services such as **Google Cloud Storage**, **Stripe**, **Firebase**, and **MailChimp**. The goal is to create a user-centric, secure, and high-performance streaming service with powerful admin tools for managing content and user subscriptions.

---

## Scope

The platform serves as a **Netflix-like application**, allowing users to browse, stream, and manage series and movies. It offers user profiles, recommendations based on preferences, payment for subscriptions, and interaction through notifications and chat.

The **admin panel** provides full control over user and content management, including content uploads, user subscriptions, and reporting.

With a focus on security and performance, the platform incorporates protection against common web vulnerabilities and integrates essential modules such as authentication, video streaming, and payment processing.

The app will be built using **Flutter** for cross-platform support, while the backend will be developed using **Django** and **Django Rest Framework**, hosted on cloud platforms like **AWS** or **Digital Ocean**.

---

## Tools and Technologies

| Domain             | Tools and Technologies                        |
|--------------------|-----------------------------------------------|
| **Backend**        | Django (Python-based framework)               |
| **API**            | Django Rest Framework (DRF)                   |
| **Mobile Apps**    | Flutter (Cross-platform for iOS and Android)  |
| **Architecture**   | MVT (Monolithic Model View Template)          |
| **Server**         | AWS or Digital Ocean                          |
| **Payments**       | Stripe (Subscription-based payments)          |
| **Video Streaming**| Google Cloud Storage / AWS S3 for video       |
| **Push Notifications** | Firebase                                 |
| **Email Services** | MailChimp                                     |

---

## Modules

### Authentication and Authorization

- Signup/Login using Email, Google, Apple, or Facebook.
- OTP Verification with 2FA (using Firebase).
- Social account linking/delinking.
- Password management and recovery.

### Admin Portal

- Manage users, content (series, episodes, movies), staff accounts, and permissions.
- Full access to system data, subscription reports, and user activity.
- Content upload and management (integrated with Google Cloud or AWS for video storage).

### User Management

- Two types of users: Admins (Super, Content Managers) and Viewers (Subscribed Users).
- Manage user profiles, viewing history, and preferences.
- Content suggestions based on user activity and preferences.

### Content Management

- Admins can upload, update, and manage series, episodes, and movies.
- Control over video streaming quality, release schedules, and category management.

### Subscription Management

- Stripe integration for subscription payments.
- Admins can offer subscription tiers, discounts, and promotions.
- Automatic renewals and invoice generation for users.

### Video Streaming Module

- High-quality video streaming with adaptive bitrate streaming.
- Content delivery using Google Cloud or AWS S3 for fast, secure, and scalable video playback.

### Notifications Module

- Push notifications for new episodes, series releases, and account updates.
- Email notifications for billing, new content, and promotions (MailChimp integration).

### In-App Messaging

- Live chat for customer support, encrypted messages for secure communication.
- Notifications for subscription updates, new episodes, and more.

### Reporting and Analytics

- Detailed reports on user activity, subscription stats, content performance, and revenue.
- Real-time analytics dashboard for admins to monitor platform performance.

### Payment Processing

- Stripe integration for handling subscription payments with various methods (Google Pay, Apple Pay, Credit Card).
- Detailed billing history, downloadable invoices for users, and payment reports for admins.

---

## Security Measures

The backend is protected against common attacks such as:

- SQL Injection
- Cross-Site Request Forgery (CSRF)
- Cross-Site Scripting (XSS)
- Clickjacking
- Directory Traversal
- Remote Code Execution (RCE)
- Insecure Direct Object Reference (IDOR)
- Session Hijacking
- Path Traversal
- Unvalidated Redirects and Forwards

---

## How to Run

### Install

```bash
git clone git@github.com:IkramKhan-DevOps/dramabox-neonapps.git
cd dramabox-neonapps
pip install -r requirements.txt
python manage.py makemigrations core users drama 
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
