pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        choice(
            name: 'DEPLOY_TARGET',
            choices: ['none', 'aws-eks', 'azure-aks', 'onprem'],
            description: 'Optional deployment credential path to prepare after the image build.'
        )
    }

    environment {
        IMAGE_NAME = 'signal-harbor'
        IMAGE_TAG = "${BUILD_NUMBER}"
        CI_KUBECONFIG = "${WORKSPACE}/.kubeconfig.ci"
    }

    stages {
        stage('Verify Toolchain') {
            steps {
                sh '''
                    chmod +x ./mvnw
                    ./mvnw -version
                    docker --version
                '''
            }
        }

        stage('Test') {
            steps {
                sh './mvnw test'
            }
        }

        stage('Prepare Runtime Secrets') {
            steps {
                withCredentials([
                    string(credentialsId: 'signal-harbor-api-key', variable: 'SIGNAL_HARBOR_API_KEY_SECRET'),
                    usernamePassword(
                        credentialsId: 'signal-harbor-postgres',
                        usernameVariable: 'SIGNAL_HARBOR_DB_USERNAME',
                        passwordVariable: 'SIGNAL_HARBOR_DB_PASSWORD'
                    )
                ]) {
                    sh '''
                        cp .env.example .env.deploy
                        set +x
                        escape_sed_replacement() {
                            printf '%s' "$1" | sed 's/[&|\\\\]/\\\\&/g'
                        }
                        API_KEY_ESCAPED="$(escape_sed_replacement "${SIGNAL_HARBOR_API_KEY_SECRET}")"
                        DB_USERNAME_ESCAPED="$(escape_sed_replacement "${SIGNAL_HARBOR_DB_USERNAME}")"
                        DB_PASSWORD_ESCAPED="$(escape_sed_replacement "${SIGNAL_HARBOR_DB_PASSWORD}")"

                        sed -i.bak "s|^SIGNAL_HARBOR_API_KEY=.*|SIGNAL_HARBOR_API_KEY=${API_KEY_ESCAPED}|" .env.deploy
                        sed -i.bak "s|^SPRING_DATASOURCE_USERNAME=.*|SPRING_DATASOURCE_USERNAME=${DB_USERNAME_ESCAPED}|" .env.deploy
                        sed -i.bak "s|^SPRING_DATASOURCE_PASSWORD=.*|SPRING_DATASOURCE_PASSWORD=${DB_PASSWORD_ESCAPED}|" .env.deploy
                        set -x
                    '''
                }
            }
        }

        stage('Package Jar') {
            steps {
                sh './mvnw -DskipTests package'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Prepare AWS EKS Credentials') {
            when {
                expression { params.DEPLOY_TARGET == 'aws-eks' }
            }
            steps {
                withCredentials([
                    [
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-deploy',
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    ],
                    file(credentialsId: 'aws-eks-kubeconfig', variable: 'KUBECONFIG_FILE')
                ]) {
                    sh '''
                        set +x
                        cp "${KUBECONFIG_FILE}" "${CI_KUBECONFIG}"
                        chmod 600 "${CI_KUBECONFIG}"
                        export KUBECONFIG="${CI_KUBECONFIG}"
                        set -x
                        aws sts get-caller-identity
                        kubectl config current-context
                        kubectl get namespace
                    '''
                }
            }
        }

        stage('Prepare Azure AKS Credentials') {
            when {
                expression { params.DEPLOY_TARGET == 'azure-aks' }
            }
            steps {
                withCredentials([
                    azureServicePrincipal(
                        credentialsId: 'azure-service-principal',
                        subscriptionIdVariable: 'AZURE_SUBSCRIPTION_ID',
                        clientIdVariable: 'AZURE_CLIENT_ID',
                        clientSecretVariable: 'AZURE_CLIENT_SECRET',
                        tenantIdVariable: 'AZURE_TENANT_ID'
                    ),
                    file(credentialsId: 'azure-aks-kubeconfig', variable: 'KUBECONFIG_FILE')
                ]) {
                    sh '''
                        set +x
                        cp "${KUBECONFIG_FILE}" "${CI_KUBECONFIG}"
                        chmod 600 "${CI_KUBECONFIG}"
                        export KUBECONFIG="${CI_KUBECONFIG}"
                        az login --service-principal \
                            --username "${AZURE_CLIENT_ID}" \
                            --password "${AZURE_CLIENT_SECRET}" \
                            --tenant "${AZURE_TENANT_ID}" >/dev/null
                        set -x
                        az account set --subscription "${AZURE_SUBSCRIPTION_ID}"
                        az account show --query id -o tsv
                        kubectl config current-context
                        kubectl get namespace
                    '''
                }
            }
        }

        stage('Prepare On-Premises SSH Credentials') {
            when {
                expression { params.DEPLOY_TARGET == 'onprem' }
            }
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'onprem-ssh-key',
                        keyFileVariable: 'ONPREM_SSH_KEY',
                        usernameVariable: 'ONPREM_SSH_USER'
                    ),
                    string(credentialsId: 'onprem-host', variable: 'ONPREM_HOST'),
                    file(credentialsId: 'onprem-kubeconfig', variable: 'KUBECONFIG_FILE')
                ]) {
                    sh '''
                        set +x
                        cp "${KUBECONFIG_FILE}" "${CI_KUBECONFIG}"
                        chmod 600 "${CI_KUBECONFIG}"
                        export KUBECONFIG="${CI_KUBECONFIG}"
                        chmod 600 "${ONPREM_SSH_KEY}"
                        set -x
                        kubectl config current-context
                        kubectl get namespace
                        ssh -i "${ONPREM_SSH_KEY}" \
                            -o BatchMode=yes \
                            -o StrictHostKeyChecking=accept-new \
                            "${ONPREM_SSH_USER}@${ONPREM_HOST}" \
                            'docker --version && kubectl version --client=true || true'
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'rm -f .env.deploy .env.deploy.bak .kubeconfig.ci'
        }
    }
}
