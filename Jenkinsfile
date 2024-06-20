pipeline {
    agent any
    
//     environment {
//         FLASK_APP = 'app.py'
//         CHROMEDRIVER_PATH = './chromedriver'
//         DOCKER_HUB_CREDENTIALS = credentials('dockerhub')
//     }

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
//
//         stage('Download docker-compose') {
//             steps {
//                 // Download docker-compose file
//                 bat 'curl -o docker-compose.yaml https://raw.githubusercontent.com/Yuvalmendel10/todo/main/docker-compose.yaml'
//             }
//         }
//
//         stage('Build docker-compose') {
//             steps {
//                 // Build Docker Compose services
//                 bat 'docker-compose build'
//             }
//         }
//
//         stage('Run docker-compose') {
//             steps {
//                 // Start Docker Compose services
//                 bat 'docker-compose up -d'
//             }
//         }
//
//         stage('Run E2E tests') {
//             steps {
//                 // Run Selenium tests against the running services
//                 bat 'python e2e.py'
//             }
//         }
//
//         stage('Stop docker-compose') {
//             steps {
//                 // Stop Docker Compose services
//                 bat 'docker-compose down'
//             }
//         }

//         stage('Login to Docker Hub') {
//             steps {
//                 // Login to Docker Hub
//                 withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
//                     bat """
//                     echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
//                     """
//                 }
//             }
//         }
//
//         stage('Upload image to Docker Hub') {
//             steps {
//                 // Push Docker image to Docker Hub
//                 bat 'docker-compose push'
//             }
//         }
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
