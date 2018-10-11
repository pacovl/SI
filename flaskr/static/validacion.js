function validarNombre(nombre) {
	return(nombre.trim().length >= 2);
}

/*TODO USAR REGEX POR DIOS QUE ESTO ES FEO*/
function validarContraseña(pass) {
	var flag1, flag2, flag3, i = 0;
	for(i=0; i<pass.length; i++){
		if(pass.charAt(i) == pass.charAt(i).toUpperCase()){
			flag1 = 1;
		}
		if('0123456789'.indexOf(pass.charAt(i)) != -1){
			flag2 = 1;
		}
		if('0123456789qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM'.indexOf(pass.charAt(i)) == -1){
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

function validar(formulario) {
	var retorno = true;
	var msj = "";

	if(! validarNombre(formulario["fnombre"].value))
	{
		formulario["fnombre"].focus();
		retorno = false;
		msj += "Escriba al menos 2 caracteres en el campo \"Nombre\".";
	}

	if(! validarContraseña(formulario["fpass"].value))
	{
		if(retorno)
		{
			formulario["fpass"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "El campo \"Contrasenia\" debe contener:\n Un n\u00FAmero entero.\n Una letra may\u00FAscula.\n Un caracter alfanumerico";
	}

	if(! validarCorreo(formulario["femail"].value))
	{
		if(retorno)
		{
			formulario["femail"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "Escriba una direcci\u00F3n de correo v\u00E1lida en el campo \"Email\".";
	}

	/*TODO FALTA VALIDAR TARJETA*/

	if(! validarSexo(formulario["fsex"].value))
	{
		if(retorno)
		{
			formulario["fsex"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "Es necesario rellenar el campo \"Sexo\"";
	}

	if(! retorno) alert(msj);

	return(retorno);
}

function validacion(formulario){
	retorno = validar(formulario);

	if(retorno){
		formulario.submit();
	}

	return retorno;
}
