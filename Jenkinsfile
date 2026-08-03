

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'network-tools'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code'
            }
        }

        stage('Validate Python Syntax') {
            steps {
                sh 'python3 -m py_compile app/Manual_logic/src/*.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -f app/Manual_logic/dockerfile -t ${IMAGE_NAME}:latest app/Manual_logic'
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
            echo 'Jenkins pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}