function validarNombre(nombre) {
	return(nombre.trim().length >= 2);
}

function validarContraseña(pass) {
	if(pass.length < 1){
		return false;
	}
	var flag1 = 0, flag2 = 0, flag3 = 0, i = 0;
	for(i=0; i<pass.length; i++){
		if(pass.charAt(i) == pass.charAt(i).toUpperCase()){
			flag1 = 1;
		}
		if('0123456789'.indexOf(pass.charAt(i)) >= 0){
			flag2 = 1;
		}

		if('qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM'.indexOf(pass.charAt(i)) >= 0){
			flag3 = 1;
		}
	}
	prod = flag1*flag2*flag3;

	if(prod == 0){
		return false;
	}

	return true;
}

function validarSexo(sexo) {
	return (sexo != "--")
}

function validarCorreo(correo) {
	return((correo.indexOf("@") > 0) && (correo.lastIndexOf("@") < correo.length-1) && (correo.indexOf("@") == correo.lastIndexOf("@")));
}

function validar(formulario, documento) {
	var retorno = true;
	var msj = "";
	if(! validarNombre(document.getElementById('nombre').value))
	{
		retorno = false;
		msj += "Escriba al menos 2 caracteres en el campo \"Nombre\".";
	}
	if(! validarContraseña(document.getElementById('pass').value))
	{
		if(retorno)
		{
			retorno = false;
		}
		else msj += "\n";
		msj += "El campo \"Contrasenia\" debe contener:\n Un n\u00FAmero entero.\n Una letra may\u00FAscula.\n Un caracter alfanumerico";
	}

	if(! validarCorreo(document.getElementById('correo').value))
	{
		if(retorno)
		{
			retorno = false;
		}
		else msj += "\n";
		msj += "Escriba una direcci\u00F3n de correo v\u00E1lida en el campo \"Email\".";
	}

	/*TODO FALTA VALIDAR TARJETA*/

	if(! validarSexo(document.getElementById('sex').value))
	{
		if(retorno)
		{
			retorno = false;
		}
		else msj += "\n";
		msj += "Es necesario rellenar el campo \"Sexo\"";
	}

	if(! retorno) alert(msj);

	return(retorno);
}

function validacion(formulario, documento){
	retorno = validar(formulario, documento);

	if(retorno){
		formulario.submit();
	}

	return retorno;
}
