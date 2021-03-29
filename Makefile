PROJECT_NAME ?= sweets-from-all-misfortunes

all:
	@echo "---------------------------------------------------------------------"
	@echo "For remote machine:"
	@echo "make ping                - Ping all available hosts"
	@echo "make venv                - Create and setup virtual environment on rm"
	@echo "make docker-login        - Login in docker on rm"
	@echo "make send-files          - Delete all old files on rm, send new"
	@echo "make deploy              - Start server on rm"
	@echo " "
	@echo "make deploy USER=user HOST=host PORT=port BUILD_NUMBER=num"
	@echo "---------------------------------------------------------------------"
	@echo "For local machine:"
	@echo "make init                - Create and start server"
	@echo "make docker-down-clear   - Stop and delete server"
	@echo "make docker-up           - Start server"
	@echo "make docker-stop         - Stop server"
	@echo "make docker-build        - Build server"
	@echo "make superuse            - Making superuser for server"
	@echo "make tests               - Start tests in container"
	@echo "make migrations          - Make migrations in container"
	@echo "---------------------------------------------------------------------"


ping:
	ansible all -m ping -i environment/hosts.yml

venv:
	export ANSIBLE_HOST_KEY_CHECKING=False
	ansible-playbook -i environment/hosts.yml environment/environment.yml -vv
	
docker-login-demo:
	ansible-playbook -i environment/hosts.yml environment/docker-login.yml -vv

send-files:
	ansible-playbook -i environment/hosts.yml send-files.yml -vv
	
deploy:
	ssh ${USER}@${HOST} -p ${PORT} 'cd src && sudo docker-compose -f docker-compose.prod.yml up --build  --remove-orphans -d'
	ssh ${USER}@${HOST} -p ${PORT} 'cd src/server && sudo docker-compose exec -T web python manage.py migrate --noinput'


init: docker-down-clear docker-pull-demo docker-build docker-up

docker-up: 
	docker-compose -f docker-compose.prod.yml up -d

docker-stop: 
	docker-compose -f docker-compose.prod.yml stop
	
docker-down-clear: 
	docker-compose -f docker-compose.prod.yml down -v --remove-orphans 
 
docker-pull-demo:
	docker-compose -f docker-compose.prod.yml pull
	
docker-build:
	docker-compose -f docker-compose.prod.yml build --pull
	

superuser:
	docker-compose exec web python manage.py createsuperuser

tests:
	docker-compose exec web python manage.py test

migrations:
	docker-compose exec web python manage.py migrate --noinput
