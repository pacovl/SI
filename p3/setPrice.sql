UPDATE
  orderdetail
SET
  price = aux.newprice
FROM
  (select POWER(0.9804, DATE_PART('year', current_date) - DATE_PART('year', O.orderdate)) * P.price as newprice, OD.orderid, OD.prod_id
                from orders as O, products as P, orderdetail as OD
                where O.orderid = OD.orderid and P.prod_id = OD.prod_id) as aux
WHERE
  orderdetail.orderid = aux.orderid and orderdetail.prod_id = aux.prod_id;
