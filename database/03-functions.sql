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

-- UPDATE Task

CREATE OR REPLACE FUNCTION public.update_task(
    intask_id integer,
    inname character varying DEFAULT NULL,
    indescription text DEFAULT NULL,
    indue_date date DEFAULT NULL,
    inidestado integer DEFAULT NULL,
    inidusuario integer DEFAULT NULL)
    RETURNS integer
    LANGUAGE 'plpgsql'
AS $BODY$
DECLARE 
    usuario_existe BOOLEAN;
    task_existe BOOLEAN;
    old_task RECORD;
BEGIN
    SELECT EXISTS (SELECT 1 FROM usuario WHERE id = inidusuario) INTO usuario_existe;

    IF usuario_existe THEN
        SELECT EXISTS (SELECT 1 FROM tasks WHERE id = intask_id) INTO task_existe;

        IF task_existe THEN
            SELECT * INTO old_task FROM tasks WHERE id = intask_id;
            
            UPDATE tasks
            SET 
                name = COALESCE(inname, old_task.name),
                description = COALESCE(indescription, old_task.description),
                due_date = COALESCE(indue_date, old_task.due_date),
                Idestado = COALESCE(inidestado, old_task.Idestado),
                Idusuario = COALESCE(inidusuario, old_task.Idusuario)
            WHERE
                id = intask_id;
            
            IF FOUND THEN
                RETURN 1; -- Se actualizó la tarea exitosamente
            ELSE
                RETURN 0; -- No se pudo actualizar la tarea
            END IF;
        ELSE
            RETURN 5002; -- El task especificado no existe
        END IF;
    ELSE
        RETURN 5001; -- El usuario especificado no existe
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

