export PGPASSWORD:=odoo
up:
	docker-compose up -d

down:
	docker-compose down

addon_scaffold:
	docker exec -it --user root plusteam-odoo-localization-web /usr/bin/odoo scaffold $(ADDON_NAME) /mnt/extra-addons

rebuild:
	docker-compose down
	docker-compose up -d --build

generate_local_coverage_report:
	docker exec -it plusteam-odoo-localization-web pytest -s --odoo-database=db_test --html=/coverage/local/report.html /mnt/extra-addons/
	docker cp plusteam-odoo-localization-web:/coverage/local coverage

generate_coverage_report:
	-docker exec -it -u root plusteam-odoo-localization-web coverage run /usr/bin/odoo -d db_test --test-enable -p 8001 --stop-after-init --log-level=test
	docker exec -it -u root plusteam-odoo-localization-web coverage html -d /coverage/all
	docker cp plusteam-odoo-localization-web:/coverage/all coverage

init_test_db:
	docker stop plusteam-odoo-localization-web
	docker exec -t plusteam-odoo-localization-db psql -U odoo -d postgres -c "DROP DATABASE IF EXISTS db_test"
	docker exec -t plusteam-odoo-localization-db psql -U odoo -d postgres -c "CREATE DATABASE db_test"
	docker start plusteam-odoo-localization-web
	docker exec -u root -t plusteam-odoo-localization-web odoo -i all -d db_test --stop-after-init --without-demo all
	docker exec -u root -t plusteam-odoo-localization-web odoo -i plus_poc -d db_test --stop-after-init
