CREATE OR REPLACE FUNCTION CONTROL.insert_codigo_recuperacao(
    p_UserID INT,
    p_codigo INT
)
RETURNS VOID AS
$$
BEGIN

    INSERT INTO CONTROL.codigos_recuperacao (UserID, criacao, codigo)
    VALUES (p_UserID, NOW(), p_codigo);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION CONTROL.delete_codigos_recuperacao(
    p_UserID INT
)
RETURNS VOID AS
$$
BEGIN

    DELETE FROM CONTROL.codigos_recuperacao
    WHERE UserID = p_UserID;
END;
$$
LANGUAGE plpgsql;