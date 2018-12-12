-- Creacion indice sobre orderdate
drop index idx_orderdate;
create index idx_orderdate on orders(orderdate);
-- Creacion indice sobre totalamount
drop index idx_totalamount;
create index idx_totalamount on orders(totalamount);

-- Consulta
select count(*) from (
    select distinct c.customerid
    from customers as c, orders as o
    where c.customerid = o.customerid and o.totalamount > 100 and DATE_PART('year', O.orderdate) = 2015 and DATE_PART('month', O.orderdate) = 04
) as clients;