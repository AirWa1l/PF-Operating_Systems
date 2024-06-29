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
