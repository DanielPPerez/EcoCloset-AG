package main

import (
	"fmt"
	"unicode"
)

type TokenType string

const (
	IDENTIFIER TokenType = "IDENTIFICADOR"
	NUMBER     TokenType = "NÚMERO"
	KEYWORD    TokenType = "PALABRA RESERVADA"
	SYMBOL     TokenType = "SÍMBOLO"
	DATATYPE   TokenType = "TIPO DE DATO"
)

type Token struct {
	Type  TokenType
	Value string
}

func isKeyword(word string) bool {
	keywords := []string{"var", "int", "float", "if", "else", "for"}
	for _, kw := range keywords {
		if word == kw {
			return true
		}
	}
	return false
}

func isDataType(word string) bool {
	dataTypes := []string{"int", "float", "string", "bool"}
	for _, dt := range dataTypes {
		if word == dt {
			return true
		}
	}
	return false
}

func Lex(input string) []Token {
	var tokens []Token
	var current string
	var currentType TokenType

	for _, char := range input {
		switch {
		case unicode.IsLetter(char):
			current += string(char)
			currentType = IDENTIFIER
		case unicode.IsDigit(char):
			current += string(char)
			currentType = NUMBER
		case unicode.IsSpace(char):
			if current != "" {
				// Clasificar palabras especiales
				if isKeyword(current) {
					currentType = KEYWORD
				} else if isDataType(current) {
					currentType = DATATYPE
				}
				tokens = append(tokens, Token{Type: currentType, Value: current})
				current = ""
			}
		case char == '=' || char == '+' || char == '-' || char == '*' || char == '/' || char == ';':
			// Agregar token anterior si existe
			if current != "" {
				if isKeyword(current) {
					currentType = KEYWORD
				} else if isDataType(current) {
					currentType = DATATYPE
				}
				tokens = append(tokens, Token{Type: currentType, Value: current})
				current = ""
			}
			// Agregar símbolo
			tokens = append(tokens, Token{Type: SYMBOL, Value: string(char)})
		}
	}

	// Agregar último token si quedó pendiente
	if current != "" {
		if isKeyword(current) {
			currentType = KEYWORD
		} else if isDataType(current) {
			currentType = DATATYPE
		}
		tokens = append(tokens, Token{Type: currentType, Value: current})
	}

	return tokens
}

func main() {
	input := " var x = 10; int y = 20; float z = 30.5;"
	tokens := Lex(input)

	fmt.Println("Tokens encontrados:")
	for _, token := range tokens {
		fmt.Printf("Tipo: %-15s Valor: %s\n", token.Type, token.Value)
	}
}