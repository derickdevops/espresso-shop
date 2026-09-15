# Espresso Shop UI Image

This repository contains only the custom frontend image used for the Espresso Shop Kubernetes lab.

It includes:

- `app.py`: a small Python web UI for Espresso Shop
- `Dockerfile`: builds the web image

The product, review, Redis, Postgres, Helm chart, and Kubernetes manifests are not included here.

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
