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

    }
}
