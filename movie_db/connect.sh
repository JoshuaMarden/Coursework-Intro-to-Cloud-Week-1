source .env
export PGPASSWORD=$DATABASE_PASSWORD
psql --host $DATABASE_IP -U $DATABASE_USERNAME -p $DATABASE_PORT $DATABASE_NAME