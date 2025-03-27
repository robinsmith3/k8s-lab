# K8s cluster for demo purpose
## Initially to show a simple static web server exposed over several instances via an nginx ingress

USAGE: kubectl apply -f ./

Deploy manifest split out to allow load balancer to distriubute evenly

## Later, to deploy a path based API backend with endpoints off the static front end
- using a scripted app called app.py on Docker
- then to apply a real database backend

## Caveats
- Avoid too many applies else LetsEncrypt will DOS you
