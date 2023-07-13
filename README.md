# UAV (Unmanned Aerial Vehicle) Rental Project

## Requirements

- Docker Engine >=18.02.0 (Check with `docker --version`)
- Docker Compose

## Setup

I do assume that you know the first couple of steps, but I did mention them anyway.

1. Clone the repository
```bash
git clone https://github.com/alfawal/uav-rental-project.git
```

2. Change directory to the project directory
```bash
cd uav-rental-project
```

3. Give the `entrypoint.sh` file the right permissions
```bash
chmod +x docker/entrypoint.sh
```

4. Build it
```bash
docker-compose -p alfawal-uav-rental -f docker/docker-compose.yaml build
```

5. Run it
```bash
docker-compose -p alfawal-uav-rental -f docker/docker-compose.yaml up
```

## Stopping the containers

```bash
docker-compose -p alfawal-uav-rental -f docker/docker-compose.yaml down
```
