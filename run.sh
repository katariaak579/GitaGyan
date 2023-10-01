#!/bin/bash


echo "Step 1: Running Docker Container..."

docker run -d  -p 8000:8000  katariaak579/gitagyan

echo "Step 2: Displaying Running Containers..."
docker ps

echo "You can access the bot on this url: http://localhost:8000/."


# End of Script
echo "Script Execution Successfully Completed."