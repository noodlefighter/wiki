

Traefik能方便地管理docker实例，代替nginx做反向代理、均衡负载，性能一般，易用为王。

快速入门：

https://docs.traefik.io/getting-started/quick-start/



## Traefik手动部署实例

`traefik/docker-compose.yml`，network_mode为host方便route到其他网络下的容器

```
version: '3'

services:
  reverse-proxy:
    # The official v2 Traefik docker image
    image: traefik:v2.10
    # Enables the web UI and tells Traefik to listen to docker
    command:
      - "--api.insecure=true"
      - "--providers.docker"
      - "--entrypoints.web.address=:38899"
    network_mode: "host"
    ports:
      # The HTTP port
      - "38899:38899"
      # The Web UI (enabled by --api.insecure=true)
      - "8080:8080"
    volumes:
      # So that Traefik can listen to the Docker events
      - /var/run/docker.sock:/var/run/docker.sock
```

另一个容器：

```
version: '3'
services:
  homepage:
    image: nginx
    container_name: "homepage"
    volumes:
      - "./nginx.conf:/etc/nginx/nginx.conf"
      - "./logs:/var/log/nginx"
      - "./html:/usr/share/nginx/html"
    restart: always
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.homepage.rule=Host(`nas.1000bug.com`)&&PathPrefix(`/`)"
      - "traefik.http.routers.homepage.entrypoints=web"
      - "traefik.http.middlewares.home-page-auth.basicauth.users=test:$$apr1$$H6uskkkW$$IgXLP6ewTrSuBkTrqE8wj/"
      - "traefik.http.routers.homepage.middlewares=home-page-auth@docker"
```

这样就为homepage创建了一个route、basicath中间件。

