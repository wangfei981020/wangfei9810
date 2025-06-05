 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"green\"}"
	
 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"red\"}"
	
 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"yellow\"}"


 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"green\"}"

 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"red\"}"

 curl -X POST http://infra-k8s-jenkins-test.slleisure.com/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"yellow\"}"



docker build -t harbor.slleisure.com/env/update-jenkins-k8s-job:20250304-135700-01 .
docker push harbor.slleisure.com/env/update-jenkins-k8s-job:20250304-135700-01