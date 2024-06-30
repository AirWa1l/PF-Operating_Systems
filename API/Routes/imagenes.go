package routes

import (
	"encoding/json"
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	"gorm.io/gorm"
)

func CreateImage(w http.ResponseWriter, r *http.Request) {

	var image models.Imagen

	err := json.NewDecoder(r.Body).Decode(&image)

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

	if err := transaction.Create(&image).Error; err != nil {
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
		"State":   http.StatusCreated,
		"success": true,
		"message": "imagen created successfully",
		"image":   image,
	}

	json.NewEncoder(w).Encode(response)
}

func GetImageID(comando string, usuario models.Usuario, db *gorm.DB, w http.ResponseWriter) {

	var imagen models.Imagen
	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Select("imagen.*").
		Joins("JOIN proceso ON proceso.id = imagen.pid AND proceso.comando = ?", comando).
		Joins("JOIN proceso_ejecucion ON proceso_ejecucion.pid = proceso.id").
		Joins("JOIN ejecucion ON ejecucion.id = proceso_ejecucion.eid").
		Joins("JOIN usuario ON ejecucion.uid = usuario.id").Where("usuario.id = ?", usuario.ID).
		First(&imagen).Error; err != nil {
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
		"message": "image find successfully",
		"Image":   imagen,
	}

	json.NewEncoder(w).Encode(response)
}
