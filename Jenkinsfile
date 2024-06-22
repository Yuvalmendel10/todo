pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.26.0'
        FLASK_APP = 'app.py'
        CHROMEDRIVER_PATH = 'chromedriver.exe'
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

//         stage('Install dependencies') {
//             steps {
//                 // Install Python dependencies from requirements.txt
//                 bat 'pip install --no-cache-dir -r requirements.txt'
//             }
//         }

        stage('Download docker compose') {
            steps {
                script {
                    bat "curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-Windows-x86_64.exe -o C:\\ProgramData\\docker-compose.exe"
                    bat 'setx PATH "%PATH%;C:\\ProgramData"'
                }
            }
        }

        stage('Build docker-compose') {
            steps {
                // Build Docker Compose services
                bat 'docker-compose build'
            }
        }

        stage('Run docker-compose')
