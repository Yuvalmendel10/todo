pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.26.0'
        FLASK_APP = 'app.py'
        CHROMEDRIVER_PATH = './chromedriver'
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub')
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository using the default SCM settings
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                // Install Python dependencies from requirements.txt
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Download docker compose') {
            steps {
                script {
                    sh "curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose"
                    sh 'chmod +x /usr/local/bin/docker-compose'
                }
            }
        }

        stage('Build docker-compose') {
            steps {
                // Build Docker Compose services
                sh 'docker-compose build'
            }
        }

        stage('Run docker-compose') {
            steps {
                // Start Docker Compose services
                sh 'docker-compose up -d'
            }
        }

        stage('Run E2E tests') {
