%option noyywrap

%%

[0-9]+          { return "Número: " + yytext; }
[a-zA-Z]+       { return "Identificador: " + yytext; }
[ \t\n]         { /* Ignorar espacios en blanco y saltos de línea */ }

.               { return "Error: Caracter no reconocido " + yytext; }

%%
