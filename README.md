# jstor-plants-image-downloader

# Flask Image Downloader and Backup to Online Storage Service(Alibaba cloud, Tencent Cloud, Qiniu cloud, etc.)

This Flask application allows users to download images by providing IDs and automatically uploads the downloaded images to Online Storage Service for backup. The downloaded images are also compressed into a ZIP file with a unique filename format.

## Features

- Batch download images using user-provided IDs.
- Store downloaded images locally.
- Automatically upload downloaded images to Online Storage Service for backup.
- Compress downloaded images into a ZIP file with a unique filename format (e.g., `abcd-20240701-123456.zip`).

## Prerequisites

- Python 3.6+
- Flask
- Your cloud service OSS SDK for Python
- Requests
- Zipfile

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/flask-image-downloader.git
    cd flask-image-downloader
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Tencent Cloud COS SDK: (You can use other service provider's SDK)

    ```bash
    pip install cos-python-sdk-v5
    ```

## Configuration

1. Replace the placeholder values in `app.py` with your Tencent Cloud COS credentials and bucket information:

    ```python
    secret_id = 'YOUR_SECRET_ID'  # Replace with your SecretId
    secret_key = 'YOUR_SECRET_KEY'  # Replace with your SecretKey
    region = 'YOUR_REGION'  # Replace with your bucket's region
    bucket = 'YOUR_BUCKET_NAME'  # Replace with your bucket name
    ```

2. Set the `UPLOAD_FOLDER` variable to the desired local directory for storing the downloaded images:

    ```python
    UPLOAD_FOLDER = '/path/to/your/upload/folder'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ```

## Running the Application

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. Enter the IDs of the images you want to download in the provided input field. Separate multiple IDs with commas.
2. Click the "下载图片" button to download the images.
3. The downloaded images will be displayed on the web page and compressed into a ZIP file with a unique filename. The ZIP file will be available for download.
4. The images will also be automatically uploaded to Tencent Cloud COS for backup.

## Nginx Configuration for HTTPS

1. Install Nginx:

    ```bash
    sudo yum install nginx
    ```

2. Install Certbot for obtaining SSL certificates:

    ```bash
    sudo yum install epel-release
    sudo yum install certbot python-certbot-nginx
    ```

3. Obtain an SSL certificate using Certbot:

    ```bash
    sudo certbot --nginx -d your_domain.com
    ```

4. Configure Nginx for HTTPS by creating or modifying the configuration file `/etc/nginx/conf.d/flask_app.conf`:

    ```nginx
    server {
        listen 80;
        server_name your_domain.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your_domain.com;

        ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            client_max_body_size 10m;
            client_body_buffer_size 128k;
        }
    }
    ```

5. Test and reload Nginx:

    ```bash
    sudo nginx -t
    sudo systemctl reload nginx
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Tencent Cloud COS SDK for Python](https://cloud.tencent.com/document/product/436/12266)
- [Requests](https://docs.python-requests.org/en/latest/)
