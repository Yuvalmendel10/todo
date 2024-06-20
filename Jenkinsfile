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

//         stage('Install dependencies') {
//             steps {
//                 // Install Python dependencies from requirements.txt
//                 sh 'pip install --no-cache-dir -r requirements.txt'
//             }
//         }

        stage('Download docker compose') {
            steps {
                script {
                    sh "sudo curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose"
                    sh 'sudo chmod +x /usr/local/bin/docker-compose'
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
            steps {
                // Run Selenium tests against the running services
                sh 'python e2e.py'
            }
        }

        stage('Stop docker-compose') {
            steps {
                // Stop Docker Compose services
                sh 'docker-compose down'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                // Login to Docker Hub
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh """
                    echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin
                    """
                }
            }
        }

        stage('Upload image to Docker Hub') {
            steps {
                // Push Docker image to Docker Hub
                sh 'docker-compose push'
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