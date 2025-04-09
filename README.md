# AI-Powered Image Segmentation and Annotation Application
Application is designed to enhance the process of image annotation and segmentation using advanced AI technologies. This tool utilizes Mask R-CNN and ResNet-50 models to detect, classify, and annotate objects within images accurately. Users can upload images to receive detailed segmentations and relevant tags, which helps in organizing and searching through large image collections.

The application features a user-friendly interface for adding textual descriptions to images and segmenting them into specific areas such as people, objects, or backgrounds. AI-driven suggestions improve the speed and accuracy of the annotation process, making it easier to classify and annotate images. Additionally, security features like two-factor authentication and user role management ensure data privacy and integrity. Comprehensive statistics tracking provides insights into annotation activities and trends.

## Screenshots
| Main page | Image page | User profile |
| -------|--------------|-----------------|
| <img src="https://github.com/user-attachments/assets/6000b9fb-d41a-49ad-ba7f-6e72949bdffc" width="400">  | <img src="https://github.com/user-attachments/assets/7692f407-d43c-44ca-a9be-61309d7ab494" width="400"> | <img src="https://github.com/user-attachments/assets/33543c75-cd16-43c5-963e-af2a5f93b728" width="400"> |

| Assigning moderator to image | Statistics | Managing moderators |
| ---------------|------------------|-----------------|
| <img src="https://github.com/user-attachments/assets/e30e3e4d-19cc-4568-b89e-eef33ce6314c" width="400"> | <img src="https://github.com/user-attachments/assets/c2db8d0b-84c1-4b15-9dfe-60ddeca0a189" width="400"> | <img src="https://github.com/user-attachments/assets/e6b8aa17-c64d-44c5-a93a-2ca2b3a5583f" width="400"> |

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
- Python >=3.8 (or >=3.12 if you wanna use fastapi2cli)
- Pip
- Node.js + npm: ^18.13.0 || ^20.9.0
- Angular CLI: Angular version 17.3.x
- PostgreSQL 16.2
- Caddy 2.8.4

### Installing
Clone the repository:
```bash
git clone https://github.com/Dawid-Nowotny/restful-ai-image-segmentation-annotation.git
```

#### Backend

1. Create the PostgreSQL Database<br />
    Create a new PostgreSQL database with the name "raisa". If you prefer a different name for the database, ensure to update the connection string in the config.py file accordingly.

2. Navigate to the backend folder:
    ```bash
    cd backend
    ```
   
3. (Optional) Create a virtual environment (recommended):
    ```bash
    # Windows
    python -m venv venv

    # Linux/macOS
    python3 -m venv venv
    ```

    Activate the virtual environment
    ```bash
    # Windows
    venv\Scripts\activate
    
    # Linux/macOS
    source venv/bin/activate
    ```

4. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

5. Migrate the tables to the database
   ```bash
   alembic upgrade head
   ```

6. Run the application:<br />
   Navigate to directory with main:
   ```bash
   cd src
   ```
    
   Using fastapi2cli
   ```bash
   fastapi dev main.py
   ```
   
   or with uvicorn
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend
1. Navigate to the frontend folder:
    ```bash
    cd frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Run the Angular application:
    ```bash
    ng serve
    ```

### Reverse proxy
Run Caddy Server:
  ```bash
  caddy run
  ```

### Runing unit tests
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
    
2. Run unit tests with pytest
   ```bash
   pytest tests
   ```

## Functionality and Security Features

### Functionalities:

- **User Management:**
  - **Login and Registration:** Secure authentication and user registration processes.

- **Image Management:**
  - **Upload Images:** Add new images to the application.
  - **Add Annotations:** Annotate images with descriptive tags and comments.
  - **Image Segmentation:** Segment images to identify distinct areas.

- **Interaction with Images:**
  - **View Images:** Browse and interact with images in the gallery.
  - **Commenting:** Add comments to images and annotations to facilitate collaboration.

- **Annotation Workflow:**
  - **Annotation Propagation:** Share annotations across images and users.

- **Search and Filtering:**
  - **Search Images by:**
    - Descriptions
    - Classes
  - **Filter Results:** Refine search results based on annotations and image attributes.

- **Analytics and Insights:**
  - **Annotation Statistics:** View statistics on existing annotations and segmentations.

### Admin Features:

- **User Activity Monitoring:** Track user activities within the application.
- **Resource Management:** Assign resources and permissions to specific users.
- **Moderator Management:** Manage moderators by assigning or revoking moderator privileges as needed.

### Security Features:

- **Authentication and Authorization:**
  - **Two-Factor Authentication (2FA):** Enhance security with two-step verification.
  - **JWT (JSON Web Tokens):** Secure token-based authentication and authorization.

- **Protection Mechanisms:**
  - **CSRF Protection:** Prevent Cross-Site Request Forgery attacks using tokens.
  - **XSS Protection:** Safeguard against Cross-Site Scripting attacks.
  - **Cookie Usage:** Securely store tokens using HTTP cookies.
 
- **Reverse Proxy:**
  - It allows the application to handle authentication tokens securely and enforce HTTP security policies.
