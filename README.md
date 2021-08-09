# CS-ERP

## Setting things up

### Run Odoo and Postgres

```shell
> docker-compose up -d
or
> make up
```

### Create custom addon scaffold

```shell
> make addon_scaffold ADDON_NAME=my_module
```

### Stop Odoo and Postgres containers
```shell
> docker-compose down
or
> make down
```
