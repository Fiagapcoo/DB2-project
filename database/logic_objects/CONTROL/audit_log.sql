CREATE OR REPLACE FUNCTION CONTROL.audit_log_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO CONTROL.audit_log (
        RecordID, 
        Modified_by,
        Field_Changed,
        Old_value,
        New_value,
        Edit_type
    ) VALUES (
        NEW.RecordID,
        NEW.Modified_by,
        TG_ARGV[0],
        TG_ARGV[1],
        TG_ARGV[2],
        TG_ARGV[3]
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_log_insert_trigger
AFTER INSERT OR UPDATE ON SOME_TABLE
FOR EACH ROW
EXECUTE PROCEDURE CONTROL.audit_log_insert_trigger_func(
    'field_name', 
    OLD.field_value, 
    NEW.field_value,
    'INSERT'
);





CREATE OR REPLACE FUNCTION CONTROL.audit_log_update_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO CONTROL.audit_log (
        RecordID,
        Modified_by,
        Field_Changed,
        Old_value,
        New_value,
        Edit_type
    ) VALUES (
        OLD.RecordID,
        NEW.Modified_by,
        TG_ARGV[0],
        TG_ARGV[1],
        TG_ARGV[2],
        TG_ARGV[3]
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_log_update_trigger
AFTER UPDATE ON SOME_TABLE
FOR EACH ROW
EXECUTE PROCEDURE CONTROL.audit_log_update_trigger_func(
    'field_name',
    OLD.field_value,
    NEW.field_value,
    'UPDATE'
);




CREATE OR REPLACE PROCEDURE CONTROL.delete_audit_log(
    p_LogID INT
)
AS $$
BEGIN
    DELETE FROM CONTROL.audit_log
    WHERE LogID = p_LogID;
END;
$$ LANGUAGE plpgsql;



--CALL CONTROL.delete_audit_log(__VALUE__);