drop function if exists set_order_amount_arg cascade;
create function set_order_amount_arg() returns trigger as $$
declare
  variable1 int;
  variable2 int;
  quantity int;
begin
    if tg_op = 'INSERT' then
      variable1 := NEW.orderid;
      variable2 := NEW.prod_id;
      quantity := NEW.quantity;

      ALTER TABLE orderdetail DISABLE TRIGGER upd_orders;

      WITH calculate_price as (select quantity * POWER(0.9804, DATE_PART('year', current_date) - DATE_PART('year', O.orderdate)) * P.price as newprice, variable1 as orderid, variable2 as prod_id
                    from orders as O, products as P
                    where O.orderid = variable1 and P.prod_id = variable2)
      UPDATE orderdetail
      SET price = newprice
      FROM (SELECT * FROM calculate_price) as aux
      WHERE aux.orderid = orderdetail.orderid and aux.prod_id = orderdetail.prod_id;


      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price) as netamount, O.orderid
          from orders as O, orderdetail as OD
          where O.orderid = OD.orderid
          group by O.orderid) as aux
      WHERE
        orders.orderid = aux.orderid and orders.orderid = variable1;

      ALTER TABLE orderdetail ENABLE TRIGGER upd_orders;

    elsif tg_op = 'UPDATE' then
      variable1 := NEW.orderid;
      variable2 := NEW.prod_id;
      quantity := NEW.quantity;

      ALTER TABLE orderdetail DISABLE TRIGGER upd_orders;

      WITH calculate_price as (select quantity * POWER(0.9804, DATE_PART('year', current_date) - DATE_PART('year', O.orderdate)) * P.price as newprice, variable1 as orderid, variable2 as prod_id
                    from orders as O, products as P
                    where O.orderid = variable1 and P.prod_id = variable2)
      UPDATE orderdetail
      SET price = newprice
      FROM (SELECT * FROM calculate_price) as aux
      WHERE aux.orderid = orderdetail.orderid and aux.prod_id = orderdetail.prod_id;

      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price) as netamount, O.orderid
          from orders as O, orderdetail as OD
          where O.orderid = OD.orderid
          group by O.orderid) as aux
      WHERE
          orders.orderid = aux.orderid and orders.orderid = NEW.orderid and orders.orderid = OLD.orderid;
      ALTER TABLE orderdetail ENABLE TRIGGER upd_orders;
      
    elsif tg_op = 'DELETE' then
      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price) as netamount, O.orderid
          from orders as O, orderdetail as OD
          where O.orderid = OD.orderid
          group by O.orderid) as aux
      WHERE
          orders.orderid = aux.orderid;
      end if;
    return NEW;
end;
$$ language plpgsql;



DROP TRIGGER IF EXISTS upd_orders ON orderdetail;
CREATE TRIGGER upd_orders
AFTER INSERT OR UPDATE OR DELETE ON orderdetail
FOR EACH ROW
EXECUTE PROCEDURE set_order_amount_arg();
