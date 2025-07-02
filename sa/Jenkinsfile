pipeline {
    agent {
        kubernetes {
            inheritFrom 'cicd-agent'
            defaultContainer 'basic'
        }
    }

    environment {
        GIT_CRED = '0bac1d39-a01e-4982-9d53-f7d8bfc212e5'
        ARGOCD_SERVER = "uat-argocd-jenkins.slileisure.com"
        LARK_WEBHOOK = "https://update-jenkins-k8s-job.slileisure.com/send_lark_card"
        GITLAB_URL = "gitlab-devops.slileisure.com/argocd/uat-k8s-platform.git"
    }

    stages {
        stage('Initialize') {
            steps {
                container('basic') {
                    script {
                        def (proj_item, new_version) = params.selected_value.split(':')
                        def userCause = currentBuild
                                         .getBuildCauses('hudson.model.Cause$UserIdCause')
                                         ?.first()
                        def build_time = new Date(currentBuild.startTimeInMillis).format("yyyy-MM-dd HH:mm:ss")
                        if (!params.only_restart && (new_version == null || new_version.isEmpty())) {
                            error("New version is required when not performing restart only")
                        }
                        env.PROJ_ITEM   = proj_item
                        env.NEW_VERSION = new_version
                        env.PROJ = (env.JOB_NAME =~ /^k8s-([^-]+-[^_]+)_/)[0][1]
                        env.BUILD_USER_ID   = userCause?.userId   ?: 'system'
                        env.BUILD_TIME = build_time
                        echo """
                        ▸ PROJ = ${env.PROJ}
                        ▸ PROJ_ITEM = ${env.PROJ_ITEM}
                        ▸ NEW_VERSION = ${env.NEW_VERSION}
                        ▸ BUILD_USER_ID = ${env.BUILD_USER_ID}
                        ▸ Only Restart = ${params.only_restart}
                        ▸ Build Time = ${build_time}
                        """
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                container('basic') {
                    git url: "https://${env.GITLAB_URL}",
                        branch: 'main',
                        credentialsId: env.GIT_CRED
                }
            }
        }

        stage('Update Code') {
            steps {
                container('basic') {
                    script {
                        sh "set +x ;git config --global --add safe.directory '${env.WORKSPACE}'"
                        def gitPath = "argocd-apps/charts/${env.PROJ}/${env.PROJ_ITEM}"
                        echo "Upgrade ${gitPath} to ${env.NEW_VERSION}"
                        def oldVersion = sh(
                            script: "set +x ;sed -n 's/^\\s*tag:\\s*\"\\(.*\\)\"/\\1/p' ${gitPath}/values.yaml",
                            returnStdout: true
                        ).trim()
                        env.OLD_VERSION = oldVersion

                        if (params.only_restart) {
                            echo "Performing service restart..."
                            def new_current = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
                            def old_current = sh(
                                script: """set +x
                                sed -n 's/.*\\([0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-9]\\{2\\}:[0-9]\\{2\\}:[0-9]\\{2\\}\\).*/\\1/p' \
                                "${gitPath}/templates/deployment.yaml" || echo 'error'""",
                                returnStdout: true
                            ).trim()

                            if (old_current != "error") {
                                sh """
                                set +x 
                                sed -i 's/manual restart at ${old_current}/manual restart at ${new_current}/g' ${gitPath}/templates/deployment.yaml
                                """
                                def message = "manual restart at ${new_current} (previous: ${old_current})"
                                env.RESTART_STATUS = "true"
                                env.NEW_VERSION = oldVersion  // 保持版本不变
                                echo "RESTART_STATUS: ${env.RESTART_STATUS}"
                                
                                // 提交重启操作
                                withCredentials([usernamePassword(
                                    credentialsId: env.GIT_CRED,
                                    usernameVariable: 'GIT_USER',
                                    passwordVariable: 'GIT_PASS'
                                )]) {
                                    sh """
                                    #!/bin/bash
                                    git config user.name  "${env.BUILD_USER_ID}"
                                    git config user.email "${env.BUILD_USER_ID}@slileisure.com"
                                    git add ${gitPath}/templates/deployment.yaml
                                    git commit -m 'Manual restart for ${env.PROJ} ${env.PROJ_ITEM} at ${new_current}'
                                    git remote set-url origin https://\$GIT_USER:\$GIT_PASS@${env.GITLAB_URL}
                                    git pull -q origin main
                                    git push -q origin main 
                                    """
                                }
                            } else {
                                error("No manual update annotations found in deployment.yaml")
                            }
                        } else {
                            if (oldVersion == env.NEW_VERSION) {
                                // Skip ArgoCD Sync and directly send Lark notification when version is unchanged
                                echo "⚠️ Version unchanged, skip ArgoCD Sync."
                                
                                // 发送 Lark 消息通知
                                def status = "orange"
                                def title = "⚠️ Version unchanged"
                                currentBuild.result = 'UNSTABLE'
                                sendLarkNotification(status, title)
                                // def payload = """
                                // {
                                //     "name": "${env.BUILD_USER_ID}",
                                //     "namespace": "${env.PROJ}",
                                //     "container": "${env.PROJ_ITEM}",
                                //     "version": "${env.NEW_VERSION}",
                                //     "uptime": "${env.BUILD_TIME}", 
                                //     "status": "${status}",
                                //     "title": "${title}"
                                // }
                                // """
                                
                                // sh """
                                //     curl -s -X POST ${env.LARK_WEBHOOK} \
                                //     -H "Content-Type: application/json" \
                                //     -d '${payload}' > /dev/null
                                // """
                                return // Exit the pipeline since the version is unchanged
                            }
                            
                            withCredentials([usernamePassword(
                                credentialsId: env.GIT_CRED,
                                usernameVariable: 'GIT_USER',
                                passwordVariable: 'GIT_PASS'
                            )]) {
                                sh """
                                #!/bin/bash
                                sed -i 's/^\\s*tag: .*/  tag: \"${env.NEW_VERSION}\"/' ${gitPath}/values.yaml
                                git config user.name  "${env.BUILD_USER_ID}"
                                git config user.email "${env.BUILD_USER_ID}@slileisure.com"
                                git add ${gitPath}/values.yaml
                                git commit -m 'Update ${env.PROJ} ${env.PROJ_ITEM} to ${env.NEW_VERSION}'
                                git remote set-url origin https://\$GIT_USER:\$GIT_PASS@${env.GITLAB_URL}
                                git pull -q origin main
                                git push -q origin main 
                                """
                            }
                        }
                    }
                }
            }
        }

        stage('ArgoCD Sync') {
            when {
                expression { 
                    env.NEW_VERSION != env.OLD_VERSION || 
                    (env.RESTART_STATUS == "true" && env.RESTART_STATUS != null) 
                }
            }
            environment {
                ARGOCD_CREDS = credentials('a950af02-f901-48e2-b92c-e308efe3552a')
            }
            steps {
                container('basic') {
                    script {
                        def argocd_app = "${env.PROJ_ITEM}-${env.PROJ}"
                        sh "argocd login ${env.ARGOCD_SERVER} --username $ARGOCD_CREDS_USR --password $ARGOCD_CREDS_PSW --grpc-web"
                        try {
                            sh "argocd app sync ${argocd_app} --grpc-web"
                            def sync_status = sh(
                                script: "argocd app get ${argocd_app} -o json --grpc-web | jq -r '.status.sync.status'",
                                returnStdout: true
                            ).trim()
                            if (sync_status != "Synced") {
                                error("ArgoCD sync failed with status: ${sync_status}")
                            }
                        } catch (Exception e) {
                            env.SYNC_FAILED = "true"
                            error("ArgoCD同步失败: ${e.message}")
                        }
                    }
                }
            }
        }

        stage('Verify Deployment') {
            when {
                expression { 
                    (env.NEW_VERSION != env.OLD_VERSION && env.SYNC_FAILED != "true") || 
                    (env.RESTART_STATUS == "true" && env.RESTART_STATUS != null) 
                }
            }
            steps {
                container('basic') {
                    script {
                        def argocd_app = "${env.PROJ_ITEM}-${env.PROJ}"
                        def max_retries = 60
                        def retry_count = 0
                        def status = "green"
                        def title = "✅✅✅ Service update successful"
                        
                        if (env.RESTART_STATUS == "true") {
                            title = "✅✅✅ Service restart successful"
                        }
                        
                        while (true) {
                            def health_status = sh(
                                script: "argocd app get ${argocd_app} -o json --grpc-web | jq -r '.status.resources[] | select(.kind==\"Deployment\") | .health.status'",
                                returnStdout: true
                            ).trim()
                            
                            if (health_status == "Healthy") {
                                echo "Deployment successful!"
                                break
                            } else if (health_status == "Degraded") {
                                status = "red"
                                title = "❌❌❌ Service update failed"
                                error("Deployment failed!")
                            }
                            
                            if (retry_count >= max_retries) {
                                status = "yellow"
                                title = "⚠️⚠️⚠️ Service startup timeout"
                                echo 'Pod startup exceeded 5 minutes'
                                break
                            }
                            
                            retry_count++
                            echo 'Waiting for pod startup...'
                            sleep 10
                        }
                        
                        sendLarkNotification(status, title)
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            script {
                // 仅在非UNSTABLE失败时发送通知
                if (currentBuild.currentResult != 'UNSTABLE') {
                    sendLarkNotification('red', '❌❌❌ Service update failed')
                }
            }
        }
    }
}

// 移至pipeline块外部
def sendLarkNotification(String status, String title) {
    def payload = """
    {
        "name": "${env.BUILD_USER_ID}",
        "namespace": "${env.PROJ}",
        "container": "${env.PROJ_ITEM}",
        "version": "${env.NEW_VERSION}",
        "uptime": "${env.BUILD_TIME}", 
        "status": "${status}",
        "title": "${title}"
    }
    """
    
    sh """
        curl -s -X POST ${env.LARK_WEBHOOK} \
        -H "Content-Type: application/json" \
        -d '${payload}' > /dev/null
    """
}
