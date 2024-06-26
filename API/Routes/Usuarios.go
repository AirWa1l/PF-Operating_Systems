package routes

import (
	"encoding/json"
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	forms "github.com/Frank-Totti/PF-Operating_Systems/Forms"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	"github.com/gorilla/mux"
	"golang.org/x/crypto/bcrypt"
)

func throwError(err error, status int, w http.ResponseWriter) {

	json.NewEncoder(w).Encode(map[string]interface{}{
		"Status": status, // Modificar el status
		"Error":  err.Error(),
	})
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

	if request.Nickname != "" {
		user.Nickname = request.Nickname
	}

	if request.Email != "" {
		user.Email = request.Email
	}

	if request.Password != "" {
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

	if err := transaction.Delete(&user).Error; err != nil {
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

	var procesos []models.Proceso
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

	if err := transaction.Table("proceso").Select("proceso.*").
		Joins("JOIN proceso_ejecucion ON proceso_ejecucion.pid = proceso.id").
		Joins("JOIN ejecucion ON ejecucion.id = proceso_ejecucion.eid").
		Joins("JOIN usuario ON ejecucion.uid = usuario.id").
		Where("usuario.id = ?", id).Find(&procesos).Error; err != nil {
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
		"State":    http.StatusOK,
		"success":  true,
		"message":  "User find successfully",
		"Procesos": procesos,
	}

	json.NewEncoder(w).Encode(response)

}

func GenerateExecution(w http.ResponseWriter, r *http.Request) {

	var request forms.JustUserID

	var user models.Usuario

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

	CreateExecution(user, config.Db, w)

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

func GenerateImage() {

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
