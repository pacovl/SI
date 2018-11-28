drop function if exists update_inventory_aux cascade;
create function update_inventory_aux(num_errors int, order_aux int) returns int as $$
begin
    if num_errors = 0 then
        --Update inventory and process
        UPDATE
            inventory
        SET stock = remainder
        FROM (SELECT P.stock - OD.quantity as remainder, P.prod_id
                FROM inventory as P, orderdetail as OD
                WHERE OD.orderid = order_aux and OD.prod_id = P.prod_id) as aux
        WHERE inventory.prod_id = aux.prod_id;

        UPDATE
            orders
        SET status = 'PROCESSED'
        WHERE orders.orderid = order_aux;
        return 1;

    else
        --Dont update inventory and make alert

        UPDATE alerts
        SET required_stock = required_stock + remainder*(-1)
        FROM (SELECT P.stock - OD.quantity as remainder, P.prod_id
                FROM inventory as P, orderdetail as OD
                WHERE OD.orderid = order_aux and OD.prod_id = P.prod_id) as aux
        WHERE remainder < 0 and aux.prod_id IN (SELECT prod_id FROM alerts);

        INSERT INTO alerts
        SELECT prod_id, remainder*(-1)
        FROM (SELECT P.stock - OD.quantity as remainder, P.prod_id
                FROM inventory as P, orderdetail as OD
                WHERE OD.orderid = order_aux and OD.prod_id = P.prod_id) as aux
        WHERE remainder < 0 and aux.prod_id NOT IN (SELECT prod_id FROM alerts);
        return 1;
    end if;
end;
$$ language plpgsql;

drop function if exists update_inventory cascade;
create function update_inventory() returns trigger as $$
DECLARE
order_aux int;
num_errors int;
retorno int;
begin
    order_aux := NEW.orderid;
    num_errors := (SELECT COUNT(aux.remainder)
        FROM (SELECT I.stock - OD.quantity as remainder
            FROM inventory as I, orderdetail as OD
            WHERE OD.orderid = order_aux and OD.prod_id = I.prod_id) as aux
        WHERE aux.remainder <= 0);

    retorno := update_inventory_aux(num_errors, order_aux);
    return NEW;
end;
$$ language plpgsql;



DROP TRIGGER IF EXISTS upd_inventory ON orders;
CREATE TRIGGER upd_inventory
AFTER UPDATE ON orders
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status and
      NEW.status = 'Paid') 
EXECUTE PROCEDURE update_inventory();