poetry lock --no-update

poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output requirements_dev.txt --without-hashes --dev
echo "requirements.txt updated"