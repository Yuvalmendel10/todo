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
                    if (isUnix()) {
                        sh "curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose"
                        sh "chmod +x /usr/local/bin/docker-compose"
                    } else {
                        bat "curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-Windows-x86_64.exe -o C:\\ProgramData\\docker-compose.exe"
                        bat 'setx PATH "%PATH%;C:\\ProgramData"'
                    }
                }
            }
        }

        stage('Build docker-compose') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker-compose --verbose build'
                    } else {
                        bat 'docker-compose --verbose build'
                    }
                }
            }
        }

        stage('Run docker-compose') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker-compose up -d'
                    } else {
                        bat 'docker-compose up -d'
                    }
                }
            }
        }

        stage('Run E2E tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'pip install --no-cache-dir -r requirements.txt'
                        sh 'python e2e.py'
                    } else {
                        bat 'pip install --no-cache-dir -r requirements.txt'
                        bat 'python e2e.py'
                    }
                }
            }
        }

        stage('Stop docker-compose') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker-compose down'
                    } else {
                        bat 'docker-compose down'
                    }
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker login -u ${DOCKER_HUB_CREDENTIALS_USR} -p ${DOCKER_HUB_CREDENTIALS_PSW}"
                    } else {
                        bat "docker login -u ${DOCKER_HUB_CREDENTIALS_USR} -p ${DOCKER_HUB_CREDENTIALS_PSW}"
                    }
                }
            }
        }

        stage('Upload image to Docker Hub') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker-compose push'
                    } else {
                        bat 'docker-compose push'
                    }
                }
            }
        }

        stage('Update Git Repository for Argo CD') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            git clone ${GIT_REPO_URL} repo
                            cd repo
                            git checkout ${GIT_BRANCH}
                            sed -i 's|image: ${DOCKER_IMAGE_NAME}:.*|image: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}|' app/deployment.yaml
                            git config user.email "yuvalmen10@gmail.com"
                            git config user.name "Yuvalmendel10"
                            git add app/deployment.yaml
                            git commit -m "Update image to ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            git push origin ${GIT_BRANCH}
                        """
                    } else {
                        bat """
                            git clone ${GIT_REPO_URL} repo
                            cd repo
                            git checkout ${GIT_BRANCH}
                            powershell -Command "(Get-Content path/to/deployment.yaml) -replace 'image: ${DOCKER_IMAGE_NAME}:.*', 'image: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}' | Set-Content path/to/deployment.yaml"
                            git config user.email "jenkins@example.com"
                            git config user.name "jenkins"
                            git add path/to/deployment.yaml
                            git commit -m "Update image to ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            git push origin ${GIT_BRANCH}
                        """
                    }
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
