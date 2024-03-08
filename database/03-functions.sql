\c db_tarea;


CREATE OR REPLACE FUNCTION public.login(
	inusername character varying,
	inuserpass character varying)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$

DECLARE existe_usuario BOOLEAN;
BEGIN
SELECT EXISTS (SELECT 1 FROM usuario WHERE name = inusername AND contraseña = inuserpass) INTO existe_usuario;
IF existe_usuario THEN	
	RETURN 1;
ELSE
	RETURN 5001;
END IF;
END;
$BODY$;


-- FUNCION PARA CREAR TAREAS

-- FUNCTION: public.create_task(character varying, text, date, integer, integer)

-- DROP FUNCTION IF EXISTS public.create_task(character varying, text, date, integer, integer);

CREATE OR REPLACE FUNCTION public.create_task(
	inname character varying,
	indescription text,
	indue_date date,
	inidestado integer,
	inusername character varying,
	inuserpass character varying)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$

DECLARE existe_usuario  BOOLEAN;
DECLARE id_usuario  integer;

BEGIN

SELECT EXISTS (SELECT 1 FROM usuario WHERE name = inusername AND contraseña = inuserpass) INTO existe_usuario;

IF existe_usuario THEN	

	SELECT id INTO id_usuario FROM usuario WHERE name = inusername AND contraseña = inuserpass;

	INSERT INTO tasks 
		(name
		, description
		, due_date
		, Idestado
		, Idusuario)
		VALUES
		(Inname
		, Indescription
		, Indue_date
		, InIdestado
		, id_usuario);
	RETURN 1;
ELSE
	RETURN 5001;
END IF;
END;
$BODY$;

-- Funcion delete segun id 

CREATE OR REPLACE FUNCTION public.delete_task(
    inId integer
)
RETURNS integer
LANGUAGE 'plpgsql'
COST 100
VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    id_existe_delete BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT 1 FROM tasks WHERE id = inId) INTO id_existe_delete;
    
    IF id_existe_delete THEN
        DELETE FROM tasks WHERE id = inId;
        RETURN 1; 
    ELSE
        RETURN 5001;
    END IF;
END;
$BODY$;

