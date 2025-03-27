# K8s cluster for demo purpose
## Initially to show a simple static web server exposed over several instances via an nginx ingress

USAGE: kubectl apply -f ./

Deploy manifest split out to allow load balancer to distriubute evenly

## Later, to deploy a path based API backend with endpoints off the static front end
- using a scripted app called app.py on Docker
- then to apply a real database backend

## Caveats
- Avoid too many applies else LetsEncrypt will DOS you

# api-backend
Create a simple API on nginx with simple backend on k8s for demos

## Forward engineered with the help of Grok
https://x.com/i/grok/share/d3CSEtNoHPjIjE4HvwnyvZmkE

## Requirements
Uses k8s, nginx ingress, nginx, _flask_, gunicon

### Caveats
- need to add path to gunicorn bin, export from .zprofile(on a Macbook): PATH="$PATH:/Users/robinsmith/Library/Python/3.9/bin"

### For testing
- flag web requests during testing: gunicorn --access-logfile - --bind 127.0.0.1:5000 api:app
- nginx.conf(on a Macbook) is here: /opt/homebrew/etc/nginx/nginx.conf
- nginx.conf for testing locally on a Mac is in this repo
- http://127.0.0.1:5000/api/items

## Docker

image at : toplard/my-flask-api
 
### Build the image
docker build -t my-flask-api:latest .
### Test it locally
docker run -p 5000:5000 my-flask-api:latest