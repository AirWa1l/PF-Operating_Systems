package main

import (
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	routes "github.com/Frank-Totti/PF-Operating_Systems/Routes"
	security "github.com/Frank-Totti/PF-Operating_Systems/Security"
	"github.com/gorilla/mux"
)

func main() {
	config.Conn()

	models.Migrate()

	OSAPP := mux.NewRouter()

	// Define subrouters
	usuarios := OSAPP.PathPrefix("/Usuarios").Subrouter()

	imagenes := OSAPP.PathPrefix("/Imagenes").Subrouter()

	///////////////////////////////////////////// Rutas para los usuarios

	// suarios.Handle("/actualizar", middleware.AuthMiddleware(http.HandlerFunc(routes.UpdateUser))).Methods("PUT")

	usuarios.HandleFunc("/crear", routes.RegisterUser).Methods("POST")
	//usuarios.HandleFunc("/actualizar", routes.UpdateUser).Methods("PUT")                     // Protected
	usuarios.Handle("/actualizar", security.Authenticate(http.HandlerFunc(routes.UpdateUser))).Methods("PUT")
	//usuarios.HandleFunc("/buscar/personal/{id}", routes.GetUser).Methods("GET")              // Protected
	usuarios.Handle("/buscar/personal/{id}", security.Authenticate(http.HandlerFunc(routes.GetUser))).Methods("GET")
	//usuarios.HandleFunc("/eliminar", routes.DeleteUser).Methods("DELETE")                    //Protected
	usuarios.Handle("/eliminar", security.Authenticate(http.HandlerFunc(routes.DeleteUser))).Methods("DELETE")
	//usuarios.HandleFunc("/buscar/ejecuciones/{id}", routes.GetUserExecutions).Methods("GET") // Protected
	usuarios.Handle("/buscar/ejecuciones/{id}", security.Authenticate(http.HandlerFunc(routes.GetUserExecutions))).Methods("GET")
	usuarios.HandleFunc("/log-in", routes.LoginUser).Methods("POST")
	//usuarios.HandleFunc("/log-out", routes.LogoutUser).Methods("GET")                            // Protected
	usuarios.Handle("/log-out", security.Authenticate(http.HandlerFunc(routes.Logout))).Methods("GET")
	//usuarios.HandleFunc("/crear/ejecución", routes.GenerateExecution).Methods("POST")            // Protedted
	usuarios.Handle("/crear/ejecución", security.Authenticate(http.HandlerFunc(routes.GenerateExecution))).Methods("POST")
	//usuarios.HandleFunc("/eliminar/ejecución", routes.GenerateDeleteExecution).Methods("DELETE") // Protected
	usuarios.Handle("/eliminar/ejecución", security.Authenticate(http.HandlerFunc(routes.GenerateDeleteExecution))).Methods("DELETE")
	//usuarios.HandleFunc("/eliminar/todo", routes.Clean).Methods("DELETE")                        // Protected
	usuarios.Handle("/eliminar/todo", security.Authenticate(http.HandlerFunc(routes.Clean))).Methods("DELETE")
	//usuarios.HandleFunc("/buscar/imagen", routes.GenerateGetImageID).Methods("POST")             // Protected
	usuarios.Handle("/buscar/imagen", security.Authenticate(http.HandlerFunc(routes.GenerateGetImageID))).Methods("POST")
	usuarios.HandleFunc("/crear/proceso", routes.CreateProcess).Methods("POST")
	usuarios.HandleFunc("/match/proceso_ejecución", routes.GeneratePro_exec).Methods("POST")

	///////////////////////////////////////////////// Rutas para las imagenes

	imagenes.HandleFunc("/crear", routes.CreateImage).Methods("POST")

	http.ListenAndServe(":3000", OSAPP)
}
