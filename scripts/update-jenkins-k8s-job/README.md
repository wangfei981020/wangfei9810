 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"green\",\"title\": \"\u2705\u2705\u2705Service update successful\"}"
   
 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"green\",\"title\": \"\u2705\u2705\u2705Service restart successful\"}"
	
 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"red\",\"title\": \"\u274C\u274C\u274C Service update failed\"}"
	
 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"yellow\",\"title\": \"\u26A0\u26A0\u26A0 Service startup over 5 minutes, check manually\"}"

 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"cesar\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"orange\",\"title\": \"\u2705\u2705\u2705 No version change\"}"


 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"green\"}"

 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"red\"}"

 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"yellow\"}"

 curl -X POST http://127.0.0.1:8080/send_lark_card \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"test\", \"namespace\": \"g101-uat\", \"container\": \"agent-api-backend\", \"version\": \"20250131092859-6\", \"uptime\": \"2025-02-07 12:34:56\",\"status\": \"orange\"}"

docker build -t harbor.slleisure.com/env/update-jenkins-k8s-job:20250306-112800-03 .
docker push harbor.slleisure.com/env/update-jenkins-k8s-job:20250306-112800-03



