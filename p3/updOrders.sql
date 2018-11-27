drop function if exists set_order_amount_arg cascade;
create function set_order_amount_arg() returns trigger as $$
begin
    if tg_op = 'INSERT' then
      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price*quantity) as netamount, O.orderid
          from orders as O, orderdetail as OD
          where O.orderid = OD.orderid
          group by O.orderid) as aux
      WHERE
        orders.orderid = aux.orderid and orders.orderid = NEW.orderid;

    elsif tg_op = 'UPDATE' then
      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price*quantity) as netamount, O.orderid
          from orders as O, orderdetail as OD
          where O.orderid = OD.orderid
          group by O.orderid) as aux
      WHERE
          orders.orderid = aux.orderid and orders.orderid = NEW.orderid and orders.orderid = OLD.orderid;
      
    elsif tg_op = 'DELETE' then
      UPDATE
          orders
      SET
          netamount = aux.netamount, totalamount=aux.netamount*(CAST(orders.tax as float)/CAST(100 as float) + 1)
      FROM
          (select SUM(price*quantity) as netamount, O.orderid
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
