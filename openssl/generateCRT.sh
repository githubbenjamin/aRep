openssl genrsa -out ca.key 2048

#这里可以使用 -subj 不用进行交互 当然还可以添加更多的信息
openssl req -x509 -new -nodes -key ca.key -subj "/CN=xxx.com" -days 5000 -out ca.crt

openssl genrsa -out server.key 2048

#这里的/cn可以是必须添加的 是服务端的域名 或者是etc/hosts中的ip别名
openssl req -new -key server.key -subj "/CN=server" -out server.csr

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 5000

#查询所生成证书的信息
openssl x509  -noout -text -in ./server.crt


// client key
openssl genrsa -out client.key 2048

openssl req -new -key client.key -subj "/CN=client" -out client.csr

echo extendedKeyUsage=clientAuth > extfile.conf

openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -extfile extfile.conf -out client.crt -days 5000 
