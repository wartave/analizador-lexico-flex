-@Comentario multilinea @-
#comentario una sola linea x=0

versa test = 0;

funcion suma(a, b) {
    retorno a + b;
}

si (x > 10) {
    imprimir("x es mayor que 10");
} sino {
    imprimir("x no es mayor que 10");
}

para (i = 0; i < 5; i = i + 1) {
    imprimir(i);
}

mientras (x < 20) {
    x = x + 1;
}

imprimir("Fin del programa");

Resultado del análisis sintáctico: [('declaracion', 'test', 0), ('func_def', 'suma', ['a', 'b'], [('return', ('a', '+', 'b'))]), ('if-else', ('x', '>', 10), [('imprimir', '"x es mayor que 10"')], [('imprimir', '"x no es mayor que 10"')]), ('for', ('=', 'i', 0), ('i', '<', 5), ('=', 'i', ('i', '+', 1)), [('imprimir', 'i')]), ('while', ('x', '<', 20), [('=', 'x', ('x', '+', 1))]), ('imprimir', '"Fin del programa"')]
