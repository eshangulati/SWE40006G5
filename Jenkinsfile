pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git branch: 'main', url: 'https://github.com/eshangulati/SWE40006G5.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t $DOCKER_IMAGE_NAME:latest .'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Run the tests using pytest in a container
                sh 'docker run --rm $DOCKER_IMAGE_NAME pytest tests/'
            }
        }
        stage('Deploy to Test Server') {
            steps {
                sshagent(['test-server-ssh']) {
                // Use SSH to connect to the test server and deploy the app
                sh """
                ssh -o StrictHostKeyChecking=no ec2-user@44.223.169.199 \\
                    'docker pull $DOCKER_IMAGE_NAME:latest && \\
                    docker stop myapp || true && \\
                    docker rm myapp || true && \\
                    docker run -d --name myapp -p 80:80 $DOCKER_IMAGE_NAME:latest'
                """
                }
            }
        }
    }
}
