package forms

import models "github.com/Frank-Totti/PF-Operating_Systems/Models"

type Execute_info struct {
	Algoritmh string
	Processes []models.Proceso
}

type Process_id_command struct {
	Id      uint
	Command string
}
