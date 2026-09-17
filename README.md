# Espresso Shop

This repository contains the custom frontend image and Helm chart used for the Espresso Shop Kubernetes lab.

It includes:

- `app.py`: a small Python web UI for Espresso Shop
- `Dockerfile`: builds the web image
- `helm/espresso-shop`: Helm chart for deploying the Espresso Shop stack

The product and review images are expected to already exist in your container runtime or registry.

## Build Locally

```bash
docker build -t devopseasylearning/s3-project01-espresso-shop:v1.0.0 .
```

## Build For Minikube

```bash
eval $(minikube docker-env)
docker build -t devopseasylearning/s3-project01-espresso-shop:v1.0.0 .
eval $(minikube docker-env -u)
```

## Restart The Web Deployment

```bash
kubectl rollout restart deployment espresso-shop-web -n espresso-shop
kubectl get pods -n espresso-shop -w
```

## Environment Variables

The UI reads these service URLs:

```bash
ProductCatalogUrl=http://espresso-shop-product-catalog-svc:8091
ReviewsUrl=http://espresso-shop-reviews-svc:8092
```

## Deploy With Helm

```bash
kubectl create namespace espresso-shop
helm install espresso-shop ./helm/espresso-shop -n espresso-shop
kubectl get pods -n espresso-shop -w
```

## Upgrade With Helm

```bash
helm upgrade espresso-shop ./helm/espresso-shop -n espresso-shop
```
