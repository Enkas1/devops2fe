pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                          branches: [[name: '*/pytestBranch']],
                          userRemoteConfigs: [[url: 'https://github.com/Vedmastaren/devops2fe.git']]
                ])
            }
        }

        stage('Setup') {
            steps {
                // Skapa en virtuell miljö och installera beroenden
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                // Linting med flake8 på specifika filer
                sh '''
                . venv/bin/activate
                flake8 app.py functions.py
                '''
            }
        }
        stage('Test') {
            steps {
                // Kör tester med pytest
                sh '''
                pytest test_database_functions.py
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Bygget lyckades!'
        }
        failure {
            echo 'Bygget misslyckades.'
        }
    }
}
