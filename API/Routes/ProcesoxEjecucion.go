package routes

import (
	"encoding/json"
	"net/http"

	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	"gorm.io/gorm"
)

func CreatePro_Exec(proceso models.Proceso, ejecucion models.Ejecución, db *gorm.DB, w http.ResponseWriter) {

	pro_exec := models.ProcesoxEjecución{Proceso: proceso, Ejecución: ejecucion, Pid: proceso.ID, Eid: ejecucion.ID}

	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Create(&pro_exec).Error; err != nil {
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
		"message": "Process_x_execution created successfully",
	}

	json.NewEncoder(w).Encode(response)

}

func GetProcessByExec(id_exec uint, db *gorm.DB, w http.ResponseWriter) []models.Proceso {

	var processes []models.Proceso

	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return nil
	}

	if err := transaction.Table("proceso").Select("proceso.*").Joins("JOIN proceso_ejecucion ON proceso_ejecucion.pid = proceso.id AND proceso_ejecucion.eid = ?", id_exec).Find(&processes).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return nil
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return nil
	}

	return processes

}

func ReusedExecution(id_exec uint, id_user uint, id_proceso uint, db *gorm.DB, w http.ResponseWriter) *models.Imagen {

	var image models.Imagen

	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return nil
	}

	if err := transaction.Preload("Proceso").Select("imagen.*").
		Joins("JOIN proceso ON proceso.id = imagen.pid AND proceso.id = ?", id_proceso).
		Joins("JOIN proceso_ejecucion ON proceso_ejecucion.pid = proceso.id").
		Joins("JOIN ejecucion ON ejecucion.id = proceso_ejecucion.eid AND ejecucion.id = ?", id_exec).
		Joins("JOIN usuario ON ejecucion.uid = usuario.id").Where("usuario.id = ?", id_user).First(&image).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return nil
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return nil
	}

	return &image

}
