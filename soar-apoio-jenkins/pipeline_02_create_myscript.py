pipeline {
    agent any

    environment {
        SCRIPT_DIR = "/var/lib/jenkins/my-project"
        SCRIPT_FILE = "${SCRIPT_DIR}/myscript.py"
    }

    stages {
        stage('Create script Python') {
            steps {
                sh '''
                    mkdir -p $SCRIPT_DIR
                    echo "📄 Create filemyscript.py on $SCRIPT_DIR..."

                    cat <<'EOF' | tee "$SCRIPT_FILE" > /dev/null
import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========================== PRODUCAO ==========================
SOAR_CONFIG = {
    "host": os.environ.get("SOAR_HOST", ""),
    "api_key": os.environ.get("SOAR_API_KEY", ""),
    "api_secret": os.environ.get("SOAR_API_SECRET", ""),
    "org_id": int(os.environ.get("SOAR_ORG_ID", 0))
}

    
if __name__ == "__main__":
    print("End of myscript.py.")
EOF

                    chmod +x "$SCRIPT_FILE"
                    echo "✅ Arquivo criado: $SCRIPT_FILE"
                '''
            }
        }
    }

    post {
        success {
            echo "🚀 Script sincronizaocao_soar_trendmicro_workbenchs.py criado com sucesso em $SCRIPT_FILE"
        }
        failure {
            echo "❌ Falha ao criar o script Python"
        }
    }
}
