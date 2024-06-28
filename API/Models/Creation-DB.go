package models

import (
	"time"

	config "github.com/Frank-Totti/PF-Operating_Systems/Config"
	"gorm.io/gorm"
)

type Usuario struct {
	gorm.Model

	Nickname string `gorm:"VARCHAR(50);unique;not null;column:nickname"`
	Email    string `gorm:"VARCHAR(50);unique;not null;column:email"`
	Password string `gorm:"VARCHAR(50);not null;column:password"`
}

func (Usuario) TableName() string {
	return "usuario"
}

type Ejecución struct {
	gorm.Model

	UID uint `gorm:"not null;column:uid"`

	CreatedAt time.Time
	DeletedAt time.Time

	Usuario Usuario `gorm:"foreignKey:uid;references:id"`
}

func (Ejecución) TableName() string {
	return "ejecucion"
}

type Proceso struct {
	gorm.Model
	Comando         string `gorm:"VARCHAR(20);not null;column:comando"`
	Tiempo_inicio   uint   `gorm:"not null;column:tiempo_inicio"`
	Tiempo_estimado uint   `gorm:"not null;column:tiempo_estimado"`
}

func (Proceso) TableName() string {
	return "proceso"
}

type Imagen struct {
	gorm.Model

	PID        uint   `gorm:"not null;column:pid"`
	ImagenID   string `gorm:"not null;unique;column:imagen_id"`
	ImagenUsed string `gorm:"VARCHAR(20);column:imagen_used"` // Represent the version, latests,...
	ImagenName string `gorm:"VARCHAR(20);column:imagen_name"` // Represent the name of the image

	Proceso Proceso `gorm:"foreignKey:pid;references:id"`
}

func (Imagen) TableName() string {
	return "imagen"
}

type ProcesoxEjecución struct {
	gorm.Model
	Pid uint `gorm:"column:pid;primaryKey;not null"`
	Eid uint `gorm:"column:eid;primaryKey"`

	Proceso   Proceso   `gorm:"foreignKey:pid;references:id;not null"`
	Ejecución Ejecución `gorm:"foreignKey:eid;references:id"`
}

func (ProcesoxEjecución) TableName() string {
	return "proceso_ejecucion"
}

func Migrate() {

	config.Db.AutoMigrate(Usuario{})
	config.Db.AutoMigrate(Ejecución{})
	config.Db.AutoMigrate(Proceso{})
	config.Db.AutoMigrate(Imagen{})
	config.Db.AutoMigrate(ProcesoxEjecución{})
}
