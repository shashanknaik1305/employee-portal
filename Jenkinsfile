```groovy
pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "984445750388"

        BACKEND_IMAGE = "employee-portal-backend"
        FRONTEND_IMAGE = "employee-portal-frontend"

        ECR_BACKEND = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${BACKEND_IMAGE}"
        ECR_FRONTEND = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${FRONTEND_IMAGE}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                sh 'docker build -t employee-portal-backend:latest ./backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh 'docker build -t employee-portal-frontend:latest ./frontend'
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr-creds',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

                    aws ecr get-login-password \
                    --region $AWS_REGION | \
                    docker login \
                    --username AWS \
                    --password-stdin \
                    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                docker tag employee-portal-backend:latest \
                $ECR_BACKEND:latest

                docker tag employee-portal-frontend:latest \
                $ECR_FRONTEND:latest
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                docker push $ECR_BACKEND:latest
                docker push $ECR_FRONTEND:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {

                sshagent(credentials: ['ec2-ssh']) {

                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@65.2.183.220 '
                    mkdir -p /home/ubuntu/employee-portal
                    '

                    scp -o StrictHostKeyChecking=no \
                    docker-compose.yml \
                    ubuntu@65.2.183.220:/home/ubuntu/employee-portal/

                    scp -o StrictHostKeyChecking=no \
                    .env \
                    ubuntu@65.2.183.220:/home/ubuntu/employee-portal/

                    ssh -o StrictHostKeyChecking=no ubuntu@65.2.183.220 '
                    aws ecr get-login-password \
                    --region ${AWS_REGION} | docker login \
                    --username AWS \
                    --password-stdin \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    cd /home/ubuntu/employee-portal

                    docker compose pull

                    docker compose up -d
                    '
                    """
                }
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
        }

        failure {
            echo "Pipeline failed!"
        }
    }
}
```
