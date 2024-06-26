package routes

import (
	"encoding/json"
	"net/http"
	"time"

	models "github.com/Frank-Totti/PF-Operating_Systems/Models"
	"gorm.io/gorm"
)

func CreateExecution(usuario models.Usuario, db *gorm.DB, w http.ResponseWriter) {

	execution := models.Ejecución{CreatedAt: time.Now(), Usuario: usuario, UID: usuario.ID}

	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Create(&execution).Error; err != nil {
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
		"message": "Execution created successfully",
		"ID":      execution.ID,
	}

	json.NewEncoder(w).Encode(response)

}

func DeleteExecution(exec models.Ejecución, db *gorm.DB, w http.ResponseWriter) {

	transaction := db.Begin()

	if err := transaction.Error; err != nil {
		transaction.Rollback()
		throwError(err, http.StatusInternalServerError, w)
		return
	}

	if err := transaction.Delete(&exec).Error; err != nil {
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
		"message": "Execution deleted successfully"}

	json.NewEncoder(w).Encode(response)

}
