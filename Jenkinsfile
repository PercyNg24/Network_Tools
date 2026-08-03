

pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_creds')
        IMAGE_NAME = 'percyng24062024/network-tools'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository'
                git branch: 'main', credentialsId: 'docker_creds', url: 'https://github.com/PercyNg24/Network_Tools.git'
            }
        }

        stage('Validate Python Syntax') {
            steps {
                sh 'python3 -m py_compile app/Manual_logic/src/*.py'
            }
        }

        stage('Check Docker') {
            steps {
                sh '''
                    which docker || exit 1
                    docker --version || exit 1
                    docker info || exit 1
                '''
            }
        }

        stage('Docker Login') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                '''
            }
        }

        stage('Pull Base Image') {
            steps {
                sh 'docker pull python:3.13.14-slim'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker.build("image"+"$BUILD_NUMBER")'
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'printf "24\\n" | python3 app/Manual_logic/src/main.py 192.168.1.10'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Docker image built and pushed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Jenkins logs.'
        }
    }
}