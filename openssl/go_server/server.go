//server端代码
package main

import (
	"fmt"
	"net/http"
	"os"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w,
		"Hi, This is an example of https service in golang!")
}

func main() {
	http.HandleFunc("/", handler)
	//http.ListenAndServe(":8080", nil)
	_, err := os.Open("cert_server/server.crt")
	if err != nil {
		panic(err)
	}
	http.ListenAndServeTLS(":8081", "cert_server/server.crt",
		"cert_server/server.key", nil)
}
