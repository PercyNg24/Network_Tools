pipeline {
    agent any

    parameters {
        string(name: 'IP_ADDRESS', defaultValue: '192.168.1.12', description: 'IP address to analyze')
        string(name: 'SUBNET_MASK', defaultValue: '/24', description: 'Subnet mask in CIDR format, for example /24')
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_creds')
        IMAGE_NAME = 'percyng24062024/network-tools'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        LATEST_TAG = 'latest'
        PATH = "/usr/local/bin:${env.PATH}" 
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
                sh 'python3 -m py_compile app/Manual_logic/src/function_def.py app/Manual_logic/src/main.py'
            }
        }

        stage('Check Docker') {
            steps {
                sh '''
                    echo "$PATH"
                    command -v docker || exit 1
                    ls -l /opt/homebrew/bin/docker /usr/local/bin/docker 2>/dev/null || true
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
                sh 'docker pull python:3.13-alpine3.20'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build --pull -f app/Manual_logic/dockerfile \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${IMAGE_NAME}:${LATEST_TAG} \
                        app/Manual_logic
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:${LATEST_TAG}
                '''
            }
        }

        stage('Pull Published Image') {
            steps {
                sh '''
                    docker pull ${IMAGE_NAME}:${LATEST_TAG}
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo "Running smoke test with IP ${params.IP_ADDRESS} and subnet ${params.SUBNET_MASK}"
                sh """
                    printf '%s\\n' '${params.SUBNET_MASK}' | docker run -it --rm ${IMAGE_NAME}:${IMAGE_TAG} '${params.IP_ADDRESS}'
                """
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Docker image built, pushed, and run successfully.'
        }
        failure {
            echo '❌ Pipeline failed. Check Jenkins logs.'
        }
    }
}