package config

import (
	"log"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// configure enviroment variables in each case

var connectionStringPassword = os.Getenv("database_password") // env variable for password

var connectionStringUser = os.Getenv("database_user") // env variable for username

var DSN = "host=localhost user=" + connectionStringUser + " password=" + connectionStringPassword + " dbname=os_db port=5432"

var Db *gorm.DB

func Conn() {
	var err error
	Db, err = gorm.Open(postgres.Open(DSN), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	} else {
		log.Println("DB connected")
	}
}
