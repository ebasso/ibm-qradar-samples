pipeline {
    agent any
    
    triggers {
        // Run every 30 minutes (server local time)
        cron('*/30 * * * *')
        // cron('* 1 * * *')
    }

    environment {
        SOAR_HOST     = "https://soar.company.com"         
        SOAR_API_KEY  = "xxxx"           
        SOAR_API_SECRET = credentials('SOAR_API_SECRET') // api token, add on jenkins credentials
        SOAR_ORG_ID  = "201"
        PYTHON_BIN   = "python3.11"      
        SCRIPT_DIR   = "/var/lib/jenkins/my-project"
        VENV_PATH    = "${SCRIPT_DIR}/venv" // path to python venv
        HTTP_PROXY   = "http://10.1.1.1"
        HTTPS_PROXY  = "http://10.1.1.1"
        NO_PROXY  = "10.1.1.100"
        SCRIPT_PATH  = "${SCRIPT_DIR}/myscript.py"
    }

    stages {
        stage('Running Script Python') {
            steps {
                sh '''
                    echo "🚀 Activating venv..."
                    source $VENV_PATH/bin/activate

                    echo "📌 Export environment variables..."
                    export SOAR_HOST="$SOAR_HOST"
                    export SOAR_API_KEY="$SOAR_API_KEY"
                    export SOAR_API_SECRET="$SOAR_API_SECRET"
                    export SOAR_ORG_ID="$SOAR_ORG_ID"

                    export HTTP_PROXY="$HTTP_PROXY"
                    export HTTPS_PROXY="$HTTPS_PROXY"
                    export NO_PROXY="$NO_PROXY"

                    echo "💻 Running myscript.py..."
                    $PYTHON_BIN "$SCRIPT_PATH"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ myscript.py run success!"
        }
        failure {
            echo "❌ Fail on run myscript.py"
        }
    }
}
