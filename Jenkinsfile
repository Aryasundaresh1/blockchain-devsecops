pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'python -m pip install -r application/requirements.txt'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r application/requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest application/test_app.py'
            }
        }
        
        stage('Docker Build') {
            steps {
                bat 'docker build -t devsecops-app .'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker rm -f devsecops-app-container || exit 0'
                bat 'docker run -d --name devsecops-app-container -p 5000:5000 devsecops-app'
            }
        }


    }
}
