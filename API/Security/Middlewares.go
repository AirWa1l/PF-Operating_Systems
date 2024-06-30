package security

import (
	"context"
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt"
)

var JwtKey = []byte("your_secret_key")

type Credentials struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type Claims struct {
	UserID       uint   `json:"user_id"`
	UserNickName string `json:"user_nickname"`
	jwt.StandardClaims
}

type contextKey string

const claimsContextKey contextKey = "claims"

func Authenticate(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var tokenStr string
		cookie, err := r.Cookie("token")
		print(r.Body)
		if err == nil {
			tokenStr = cookie.Value
		} else {
			// Si no hay cookie, intenta obtener el token del encabezado de autorización
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			bearerToken := strings.Split(authHeader, " ")
			if len(bearerToken) != 2 {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			tokenStr = bearerToken[1]
		}

		claims := &Claims{}
		token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
			return JwtKey, nil
		})

		if err != nil {
			if err == jwt.ErrSignatureInvalid {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}

		if !token.Valid {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}

		ctx := r.Context()
		ctx = context.WithValue(ctx, claimsContextKey, claims)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

/*
func Authenticate(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("token")
		if err != nil {
			if err == http.ErrNoCookie {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}

		tokenStr := cookie.Value
		claims := &Claims{}

		token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
			return JwtKey, nil
		})

		if err != nil {
			if err == jwt.ErrSignatureInvalid {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}

		if !token.Valid {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}

		ctx := r.Context()
		ctx = context.WithValue(ctx, claimsContextKey, claims)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
*/
