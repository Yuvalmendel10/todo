pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.26.0'
        FLASK_APP = 'app.py'
        CHROMEDRIVER_PATH = 'chromedriver.exe'
        // not secure - change it! -
        DOCKER_HUB_USERNAME = "yuvalmendel10"
        DOCKER_HUB_PASSWORD = "YuvalDocker10"
        DOCKER_IMAGE_NAME = 'yuvalmendel10/todo:latest'
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig')
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
                bat 'docker-compose --verbose build'
            }
        }

        stage('Run docker-compose') {
            steps {
                bat 'docker-compose up -d'
            }
        }

        stage('Run E2E tests') {
            steps {
                bat 'pip install --no-cache-dir -r requirements.txt'
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
                bat "docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}"
            }
        }

        stage('Upload image to Docker Hub') {
            steps {
                bat 'docker-compose push'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    bat '''
                        set KUBECONFIG=%KUBECONFIG%
                        kubectl apply -f todo.yaml
                        kubectl apply -f todo-service.yaml
                    '''
                }
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
