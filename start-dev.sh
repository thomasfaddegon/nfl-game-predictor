#!/bin/bash
echo "Starting Flask app..."
export FLASK_APP=api.py
export FLASK_ENV=development
flask run &

echo "Starting JavaScript dev server..."
cd front-end
npm run dev &

# Return to the original directory
cd ..


# use './start-dev.sh' to start the app