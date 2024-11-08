# Quantum Advanced Inc.

This repository contains the source code and documentation for Quantum Advanced Inc., a cutting-edge quantum computing and DeFi company.

## Project Structure

- `src/control_room/`: Contains the main application code
- `docs/`: Documentation files
- `marketing/`: Marketing materials

## Features

- User authentication
- Quantum computing demo using Qiskit
- Containerized application using Docker
- CI/CD pipeline using GitHub Actions
- Serverless deployment configuration for AWS Lambda

## Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python src/control_room/app.py`

## Docker Development

1. Build the Docker image: `docker build -t quantum-advanced-inc .`
2. Run the container: `docker run -p 5000:5000 quantum-advanced-inc`

## Static Site Generation

Run `python generate_static_site.py` to create a static version of the site in the `static_site` directory.

## Deployment Options

1. Heroku: Use the provided Procfile
2. AWS Lambda: Use the serverless.yml configuration with Serverless Framework
3. Any WSGI-compatible server: Use the wsgi.py file

## CI/CD

The GitHub Actions workflow in `.github/workflows/ci_cd.yml` handles continuous integration and deployment.

## Contact

For any inquiries, please contact: ianmcinturff9@gmail.com
