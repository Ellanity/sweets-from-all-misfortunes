# sweets-from-all-misfortunes
Приложение упаковано в Docker-контейнер и разворачивается с помощью Ansible.
Управление REST API сервисом происходит при помощи make команд.

Скачайте репозиторий на свою локальную машину.

В корневой папке, где файл Makefile, присутствуют команды:
make - все команды с кратким описанием
make ping
make venv
make docker-login
make send-files
make init
make docker-down-clear
make docker-up
make docker-stop
make docker-build

make superuser
make tests
make migrations

Чтобы развернуть и запустить сервис на удаленной машине, в файле environment/hosts.ini настройте сервер, на котором будет запускаться сервис.
Для развертки на удаленной машине требуется прописать команды: make ping, make venv, make send-files, make-deploy.
Так как подключение происходит по ssh. Требуются пользователь и пароль для удаленной машины.
Синтаксис команды make deploy: make deploy USER=user HOST=host PORT=port BUILD_NUMBER=num

Для развертки на локальной машине: make init.


