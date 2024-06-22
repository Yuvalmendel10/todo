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
            // Verify Docker is running
                bat 'docker --version'
                bat 'docker-compose --version'

                bat 'docker-compose build'
            }
        }

        stage('Run docker-compose') {
            steps {
                bat 'docker-compose up -d'
            }
        }

        stage('Run E2E tests') {
            steps {
                bat 'python e2e.py'
            }
        }

        stage('Stop docker-compose') {
            steps {
                bat 'docker-compose down'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    bat """
                    echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                    """
                }
            }
        }

        stage('Upload image to Docker Hub') {
            steps {
                bat 'docker-compose push'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Clean up resources if needed.'
        }
        failure {
            echo 'Pipeline failed! Clean up resources if needed.'
        }
    }
}