docker build --network=host -t my-mysql-container .

docker run -p 3306:3306 -d my-mysql-container