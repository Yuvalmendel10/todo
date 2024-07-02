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
        // KUBECONFIG_CREDENTIALS = credentials('kubeconfig')
        GIT_REPO_URL = 'https://github.com/Yuvalmendel10/todo-argocd.git'
        GIT_BRANCH = 'main'
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


         stage('Update Argo CD Git Repository') {
            steps {
                script {
                    bat """
                        git clone ${GIT_REPO_URL} repo
                        cd repo
                        git checkout ${GIT_BRANCH}
                        powershell -Command "(Get-Content app/deployment.yaml) -replace 'image: ${DOCKER_IMAGE_NAME}:.*', 'image: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}' | Set-Content app/deployment.yaml"
                        git config user.email "yuvalmen10@gmail.com"
                        git config user.name "Yuvalmendel10"
                        git add app/deployment.yaml
                        git commit -m "Update image to ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                        git push origin ${GIT_BRANCH}
                    """
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
