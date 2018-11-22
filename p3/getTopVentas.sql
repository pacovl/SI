drop function if exists getTopVentas cascade;
CREATE FUNCTION getTopVentas(a int)  
RETURNS TABLE (
    year float,
    movieTitle varchar,
    ventas bigint
)
AS $$
begin
RETURN  query
    select distinct on (year) DATE_PART('year', O.orderdate) as year, M.movieTitle as Pelicula, SUM(OD.quantity) as ventas
    from imdb_movies as M, products as P, orderdetail as OD, orders as O
    where P.movieid=M.movieid and OD.prod_id=P.prod_id and O.orderid = OD.orderid and DATE_PART('year', O.orderdate) >= a
    group by O.orderdate, M.movieTitle
    order by year, ventas DESC;
END; $$  

LANGUAGE 'plpgsql';
