# Deploying to minikube

From the deployment folder:

1. Run `minikube-start.sh` to start minikube and mount the shared directory (needs to stay open for mount to work)
2. Run `deploy-charts-minikube.sh` to deploy the prometheus stack
3. Create a file `secrets.yaml` in `./k8s/` with contents:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: api-keys
   type: Opaque
   stringData:
     API_KEY: <api-keys delimited by ','>
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: github-api-key
   type: Opaque
   stringData:
     GITHUB_ACCESS_TOKEN: <Github API Token>
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: drive-secrets
   type: Opaque
   stringData:
     DRIVE_SVC_JSON: >
       <contents of gdrive secret json file>
   Make sure to replace `<api-keys delimited by ','>` by the actual api keys.
4. Run `kubectl apply -f deployment/k8s` to deploy the ingress and inference services
5. If you now run `kubectl get pods` everything should be either starting/running
6. To monitor the processes follow the steps below

## Enabling access to the applications
We tried the Minikube ingress but didn't get it to work as we wanted it to. Therefore, to access the applications (Inference frontend, Grafana, Prometheus) they need to be port-forwarded to the host:
 - Inference frontend: <br>`kubectl port-forward svc/inference-frontend-service 8080:8080`
   The web-frontend can now be accessed at: http://localhost:8080/question/
 - Grafana: <br> `kubectl port-forward svc/promstack-grafana 3000:80`
   - To access the dashboards they first need to be imported:
     1. Go to http://localhost:3000
     2. login with username: admin, password: prom-operator
     3. Hover to '+' (create) button in the left button pane, click import
     4. Copy the contents from [`scraping-dashboard.json`](./scraping-dashboard.json) into the text box.
     5. Click load
     6. Click import
     7. Repeat 4-6 for [`train-dashboard.json`](./scraping-dashboard.json)
     8. Both dashboards should now be available in the dashboard overview (Names: Train overview, Scraping overview)

 - Prometheus: 
  <br>`kubectl port-forward svc/promstack-kube-prometheus-prometheus 9090:9090`

## Known issues
 - The symlink/mount to the host disk is unreliable. If you get an error like:
    ```
   failed to try resolving symlinks in path "/var/log/pods/default_scraping-deployment-6b944fd646-f7pwf_c459c107-5188-4f69-a8da-a9502ef92ee7/scraping-app/0.log": lstat /var/log/pods/default_scraping-deployment-6b944fd646-f7pwf_c459c107-5188-4f69-a8da-a9502ef92ee7/scraping-app/0.log: no such file or directory
   ```
  restarting minikube will likely fix it. If not `minikube` delete followed by a restart might.
