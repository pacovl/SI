drop function if exists getTopMonths cascade;
CREATE FUNCTION getTopMonths(umbral_A int, umbral_B numeric)  
RETURNS TABLE (
    year float,
    month float,
    num_ventas numeric,
    ingresos_totales numeric
)
AS $$
begin
RETURN  query
    SELECT *
    FROM (SELECT DATE_PART('year', O.orderdate) as year, 
                DATE_PART('month', O.orderdate) as month,
                SUM(aux.num_prod) as num_ventas,
                SUM(O.totalamount) as ingresos_totales
            FROM
                orders as O,
                (SELECT SUM(OD.quantity) as num_prod, O.orderid
                FROM orders as O, orderdetail as OD
                WHERE O.orderid = OD.orderid
                GROUP BY O.orderid) as aux
            WHERE
                aux.orderid = O.orderid
            GROUP BY DATE_PART('year', O.orderdate), DATE_PART('month', O.orderdate)) as proxy
    WHERE proxy.num_ventas > umbral_A or proxy.ingresos_totales > umbral_B
    ORDER BY year desc, month;
END; $$  

LANGUAGE 'plpgsql';

