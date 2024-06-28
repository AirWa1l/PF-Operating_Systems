package routes

import (
	"encoding/json"
	"log"
	"net/http"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
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
	log.Println(proceso.ID)

	response := map[string]interface{}{
		"Status":  http.StatusCreated,
		"success": true,
		"message": "Process created successfully",
		"ID":      proceso.ID,
	}

	json.NewEncoder(w).Encode(response)

}
