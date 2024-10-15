pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'myapp'
        TEST_SERVER_IP = '44.223.169.199'
        PRODUCTION_SERVER_IP = '3.213.22.15'
        SSH_KEY_PATH = '/var/lib/jenkins/.ssh/id_rsa'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/eshangulati/SWE40006G5.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE_NAME:latest .'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Run the tests inside the Docker container
                sh 'docker run --rm $DOCKER_IMAGE_NAME pytest tests/'
            }
        }


        stage('Deploy to Test Server') {
            steps {
                script {
                    // Directly SSH using the private key
                    sh """
                    ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ec2-user@$TEST_SERVER_IP \\
                        'docker pull buffy1809/myapp:latest && \\
                        docker stop myapp || true && \\
                        docker rm myapp || true && \\
                        docker run -d --name myapp -p 80:80 buffy1809/myapp:latest'
                    """
                }
            }
        }

        stage('Deploy to Production Server') {
            steps {
                script {
                    sh """
                    ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ec2-user@$PRODUCTION_SERVER_IP \\
                        'docker pull buffy1809/myapp:latest && \\
                        docker stop myapp || true && \\
                        docker rm myapp || true && \\
                        docker run -d --name myapp -p 80:80 buffy1809/myapp:latest'
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
