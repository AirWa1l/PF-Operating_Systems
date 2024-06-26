package forms

type SearchCommand struct {
	ID      uint   `json:"id"`
	Comando string `json:"comando"`
}

type ExecUser struct {
	UID uint `json:"uid"`
	EID uint `json:"eid"`
}

type JustUserID struct {
	ID uint `json:"id"`
}

type SearchUser struct {
	ID       uint   `json:"id"`
	Nickname string `json:"Nickname"`
	Email    string `json:"Email"`
	Password string `json:"Password"`
}

type DeleteUser struct {
	ID       uint   `json:"id"`
	Password string `json:"Password"`
}
