# [jimshew/docker-evilginx](https://github.com/jimshew/docker-evilginx)

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/jimshew/docker-evilginx)
[![CI](https://github.com/jimshew/docker-evilginx/workflows/Docker/badge.svg?event=push)](https://github.com/jimshew/docker-evilginx/actions?query=workflow%3ADocker)
![License](https://img.shields.io/github/license/jimshew/docker-evilginx)
![Commit](https://img.shields.io/github/last-commit/jimshew/docker-evilginx)

[Evilginx2](https://github.com/kgretzky/evilginx2) - Standalone man-in-the-middle attack framework used for phishing login credentials along with session cookies, allowing for the bypass of 2-factor authentication

![Evilginx2](https://raw.githubusercontent.com/kgretzky/evilginx2/master/media/img/evilginx2-logo-512.png)

[Original Docker-Evilginx2](https://github.com/warhorse/docker-evilginx2) - Previous Dockerized work on evilginx2 (but version is 3.2.0 at time of this fork). 

This repository is designed to be separate as it will likely have adjustments only needed for the SANS Institute SEC660: Advanced Penetration Testing and Exploit Writing course.

## Usage

Here are some example snippets to help you get started creating a container.

### docker

```
docker create \
  --name=evilginx \
  -p 10.50.50.50:443:443 \
  -p 10.50.50.50:80:80 \
  -p 7443 \
  -v /opt/evilginx/config:/config \
  -v /opt/evilginx/phishlets:/phishlets 
  --restart unless-stopped \
  jimshew/evilginx
```

### docker-compose

Compatible with docker-compose v2 schemas.

```
---  -p 10.50.50.50:80:80 \

version: "2"
services:
  evilginx:
    image: jimshew/evilginx
    container_name: evilginx
    environment:
      - TZ=Europe/London
    volumes:
      - /opt/evilginx/config:/config
      - /opt/evilginx/phishlets:/phishlets
    ports:
      - 10.50.50.50:443:443
      - 10.50.50.50:80:80
      - 7443:7443
    restart: unless-stopped
```

## Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8080:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8080` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 10.50.50.50:80:80` | Use host's IP 10.50.50.50 and pass the port for HTTP traffic |
| `-p 10.50.50.50:443:443` | Use host's IP 10.50.50.50 and pass the port for HTTPS traffic |
| `-e TZ=Europe/London` | Specify a timezone to use EG Europe/London|
| `-v /config` | evilginx2 configs |
| `-v /phishlets` | evilginx2 phishlets |

### Docker start

```
docker start evilginx
```

## Application Setup

Access the webui at `<your-ip>:7443`, for more information check out [evilginx2](https://github.com/kgretzky/evilginx2).

## Support Info

* Shell access whilst the container is running: `docker exec -it evilginx /bin/bash`
* To monitor the logs of the container in realtime: `docker logs -f evilginx`

## Building locally

If you want to make local modifications to these images for development purposes or just to customize the logic:
```
git clone https://github.com/jimshew/docker-evilginx.git
cd docker-evilginx
docker build \
  --no-cache \
  --pull \
  -t jimshew/evilginx2:latest .
```
## Versions

* **02.13.20:** - First Push
