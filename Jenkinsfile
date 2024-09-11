pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                          branches: [[name: '*/dev']],
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
                pip list
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
                . venv/bin/activate
                python -m pytest test/test_database_functions.py --maxfail=1 --disable-warnings -q
                python -m pytest test/test_functions.py
                '''
            }
        }
        
    }

    post {
        always {
            // Rensa arbetsytan efter varje byggprocess
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
