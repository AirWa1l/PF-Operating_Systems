package main

import (
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	routes "github.com/Frank-Totti/PF-Operating_Systems/Routes"
	"github.com/gorilla/mux"
)

func main() {
	config.Conn()

	models.Migrate()

	OSAPP := mux.NewRouter()

	///////////////////////////////////////////// Rutas para los usuarios
	usuarios := OSAPP.PathPrefix("/Usuarios").Subrouter()

	usuarios.HandleFunc("/crear", routes.RegisterUser).Methods("POST")
	usuarios.HandleFunc("/actualizar", routes.UpdateUser).Methods("PUT")
	usuarios.HandleFunc("/buscar/personal/{id}", routes.GetUser).Methods("GET")
	usuarios.HandleFunc("/eliminar", routes.DeleteUser).Methods("DELETE")
	usuarios.HandleFunc("/buscar/ejecuciones/{id}", routes.GetUserExecutions).Methods("GET")

	http.ListenAndServe(":3000", OSAPP)
}
