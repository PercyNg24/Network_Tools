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

        stage('Docker Login') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build -f app/Manual_logic/dockerfile \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        app/Manual_logic
                '''
            }
        }

        stage('Run Container') {
            steps {
                echo "Running container with IP ${params.IP_ADDRESS} and subnet ${params.SUBNET_MASK}"
                sh '''
                    set +e
                    CONTAINER_NAME="network-tools-${BUILD_NUMBER}"
                    docker run --name "$CONTAINER_NAME" ${IMAGE_NAME}:${IMAGE_TAG} '${params.IP_ADDRESS}' '${params.SUBNET_MASK}'
                    status=$?
                    docker rm -f "$CONTAINER_NAME" || true
                    exit $status
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Docker image built and run successfully.'
        }
        failure {
            echo '❌ Pipeline failed. Check Jenkins logs.'
        }
    }
}