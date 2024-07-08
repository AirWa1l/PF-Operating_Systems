package routes

import (
	"encoding/json"
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	forms "github.com/Frank-Totti/PF-Operating_Systems/Forms"
	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
)

func CreateProcess(w http.ResponseWriter, r *http.Request) {

	var proceso models.Proceso

	err := json.NewDecoder(r.Body).Decode(&proceso)

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

	if err := transaction.Table("proceso").Where("proceso.comando = ? AND proceso.tiempo_inicio = ? AND proceso.tiempo_estimado = ?", proceso.Comando, proceso.Tiempo_inicio, proceso.Tiempo_estimado).First(&proceso).Error; err != nil {
		if err := transaction.Create(&proceso).Error; err != nil {
			transaction.Rollback()
			throwError(err, http.StatusInternalServerError, w)
			return
		}
	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"Status":  http.StatusCreated,
		"success": true,
		"message": "Process created successfully",
		"ID":      proceso.ID,
	}

	json.NewEncoder(w).Encode(response)

}

func GetProcessesByExec(w http.ResponseWriter, r *http.Request) {

	var request forms.ExecUser

	var processes []models.Proceso

	map_to_return := map[string]models.Imagen{}

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

	if err := transaction.Table("proceso").Select("proceso.*").Joins("JOIN proceso_ejecucion ON proceso_ejecucion.pid = proceso.id").Joins("JOIN ejecucion ON ejecucion.id = proceso_ejecucion.eid AND ejecucion.id = ?", request.EID).Where("ejecucion.deleted_at IS NULL").Find(&processes).Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusNotFound, w)
		return
	}

	for i := 0; i < len(processes); i++ {

		map_to_return[processes[i].Comando] = *ReusedExecution(request.EID, request.UID, processes[i].ID, config.Db, w)

	}

	if err := transaction.Commit().Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	response := map[string]interface{}{
		"Status":    http.StatusOK,
		"success":   true,
		"message":   "Match Process - Image ok",
		"Processes": processes,
		"Match":     map_to_return,
	}

	//log.Println(response)

	json.NewEncoder(w).Encode(response)

}
