CREATE OR REPLACE FUNCTION datetime_func(p_date IN OUT DATE)
RETURN DATE IS
BEGIN
    p_date := p_date + 10;
    RETURN p_date;
END datetime_func;
