package routes

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	forms "github.com/Frank-Totti/PF-Operating_Systems/Forms"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	security "github.com/Frank-Totti/PF-Operating_Systems/Security"
	"github.com/golang-jwt/jwt"
	"github.com/gorilla/mux"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

func throwError(err error, status int, w http.ResponseWriter) {

	json.NewEncoder(w).Encode(map[string]interface{}{
		"Status": status, // Modificar el status
		"succes": false,
		"Error":  err.Error(),
	})
}

func LoginUser(w http.ResponseWriter, r *http.Request) {
	var creds security.Credentials

	log.Println("Logeado pa")

	if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	var user models.Usuario
	if err := transaction.Where("email = ?", creds.Email).First(&user).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			http.Error(w, "User not found", http.StatusUnauthorized)
		} else {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		}
		return
	}

	err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(creds.Password))
	if err != nil {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}

	expirationTime := time.Now().Add(24 * time.Hour)
	claims := &security.Claims{
		UserID:       user.ID,
		UserNickName: user.Nickname,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(security.JwtKey)
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	http.SetCookie(w, &http.Cookie{
		Name:    "token",
		Value:   tokenString,
		Expires: expirationTime,
	})

	json.NewEncoder(w).Encode(map[string]interface{}{
		"success":     true,
		"State":       http.StatusOK,
		"tokenString": tokenString,
		"token":       token,
	})
}

func Logout(w http.ResponseWriter, r *http.Request) {
	// Eliminar cookie de token
	log.Println("Deslogeado pa")

	http.SetCookie(w, &http.Cookie{
		Name:    "token",
		Value:   "",
		Expires: time.Now().Add(-time.Hour),
	})

	reponse := map[string]interface{}{
		"success": true,
		"State":   http.StatusOK,
		"message": "Logout sucefully",
	}

	json.NewEncoder(w).Encode(reponse)
}

func RegisterUser(w http.ResponseWriter, r *http.Request) {

	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&user)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	Cpassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)

	if err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}
	user.Password = string(Cpassword)

	if err := transaction.Create(&user).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"Status":  http.StatusCreated,
		"success": true,
		"message": "User created successfully",
	}

	json.NewEncoder(w).Encode(response)

}

func UpdateUser(w http.ResponseWriter, r *http.Request) {
	var request forms.SearchUser
	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").Where("usuario.id = ?", request.ID).First(&user).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if request.Nickname != "default" {
		user.Nickname = request.Nickname
	}

	if request.Email != "default" {
		user.Email = request.Email
	}

	if request.Password != "default" {
		cPassword, err := bcrypt.GenerateFromPassword([]byte(request.Password), bcrypt.DefaultCost)

		if err != nil {
			transaction.Rollback()
			throwError(err, http.StatusInternalServerError, w)
			return
		}

		user.Password = string(cPassword)
	}

	if err := transaction.Save(&user).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"State":   http.StatusOK,
		"success": true,
		"message": "User update successfully",
	}

	json.NewEncoder(w).Encode(response)

}

func GetUser(w http.ResponseWriter, r *http.Request) {

	params := mux.Vars(r)

	var user models.Usuario

	id := params["id"]

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").First(&user, id).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"State":   http.StatusOK,
		"success": true,
		"message": "User find successfully",
		"user":    user,
	}

	json.NewEncoder(w).Encode(response)

}

func DeleteUser(w http.ResponseWriter, r *http.Request) {

	var request forms.DeleteUser

	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").First(&user, request.ID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(request.Password)); err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Unscoped().Delete(&user).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"State":   http.StatusNoContent,
		"success": true,
		"message": "User delete successfully",
	}
	json.NewEncoder(w).Encode(response)

}

func GetUserExecutions(w http.ResponseWriter, r *http.Request) {

	//var procesos []models.ProcesoxEjecución

	var ejecuciones []models.Ejecución

	params := mux.Vars(r)

	var user models.Usuario

	id := params["id"]

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").First(&user, id).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Preload("Usuario").Table("ejecucion").Joins("JOIN usuario ON usuario.id = ejecucion.uid").Where("usuario.id = ?", id).Find(&ejecuciones).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	map_exec_processes := map[uint]forms.Execute_info{}

	for i := 0; i < len(ejecuciones); i++ {
		actual_execution_id := ejecuciones[i].ID

		map_exec_processes[actual_execution_id] = *GetProcessByExec(actual_execution_id, config.Db, w)

	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"State":    http.StatusOK,
		"success":  true,
		"message":  "User find successfully",
		"Procesos": map_exec_processes,
	}

	json.NewEncoder(w).Encode(response)

}

func GenerateExecution(w http.ResponseWriter, r *http.Request) {

	var request forms.UserID_Algorithm

	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	log.Println(request)

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").First(&user, request.ID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	CreateExecution(user, request.Algorithm, config.Db, w)

}

func GenerateDeleteExecution(w http.ResponseWriter, r *http.Request) {

	var request forms.ExecUser

	var user models.Usuario

	var exec models.Ejecución

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}
	if err := transaction.Table("usuario").First(&user, request.UID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Table("ejecucion").First(&exec, request.EID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	DeleteExecution(exec, config.Db, w)
}

func Clean(w http.ResponseWriter, r *http.Request) {

	var request forms.JustUserID

	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}
	if err := transaction.Table("usuario").First(&user, request.ID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Where("ejecucion.uid = ?", request.ID).Delete(&models.Ejecución{}).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"State":   http.StatusNoContent,
		"success": true,
		"message": "Clean successfully",
	}
	json.NewEncoder(w).Encode(response)

}

func GenerateGetImageID(w http.ResponseWriter, r *http.Request) {

	var request forms.SearchCommand

	var user models.Usuario

	err := json.NewDecoder(r.Body).Decode(&request)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Table("usuario").First(&user, request.ID).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	GetImageID(request.Comando, user, config.Db, w)

}

func GeneratePro_exec(w http.ResponseWriter, r *http.Request) {

	var pro_exec forms.Union

	var proceso models.Proceso

	var ejecucion models.Ejecución

	err := json.NewDecoder(r.Body).Decode(&pro_exec)

	if err != nil {
		throwError(err, http.StatusBadRequest, w)
		return
	}

	//log.Println(pro_exec)

	transaction := config.Db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Where("proceso.id = ?", pro_exec.Pid).First(&proceso).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Where("ejecucion.id = ?", pro_exec.Eid).First(&ejecucion).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	CreatePro_Exec(proceso, ejecucion, config.Db, w)

}

/*
REGISTER USER
{
  "Nickname":"Susana Valencia",
  "Email":"SusanaPrincesa@gmail.com",
  "Password":"Tomacito1503"

}

*/
