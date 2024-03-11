# Horticulture Pest and Disease Biosecurity Guide

## Overview
This Flask Python web application serves as a comprehensive guide to horticulture pests and diseases, focusing on biosecurity in New Zealand. It features a responsive design that reflects a horticulture theme and includes a secure login system with role-based dashboards for Horticulturalists, Staff, and Administrators. 

## Features
- **Home Page:** An attractive landing page with a horticulture theme, offering links to login and registration.
- **User Login and Registration:** Secure login functionality with password hashing and salting, alongside a registration option for new Horticulturalist users.
- **Role-Based Access Control:** Defines three user roles with specific access levels to various features and pages.
  - **Horticulturalists** can manage their profile and view detailed guides on pests and diseases.
  - **Staff** have the ability to manage their profile, view Horticulturalists profiles, and fully manage the guide.
  - **Administrators** enjoy full access to the system, including user and guide management.
- **Responsive Design:** Ensures a seamless experience across various devices, embodying a horticulture-inspired aesthetic.
- **Data Security:** Emphasizes secure storage and management of user credentials and sensitive biosecurity data.

## Data Requirements
The application database includes profiles for at least 5 Horticulturalists, 3 Staff members, one Administrator, and details on 20 horticulture pests/diseases, distinguishing those present in and absent from NZ.
