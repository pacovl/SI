drop function if exists update_inventory cascade;
create function update_inventory() returns trigger as $$
declare
order_aux int;
begin
    if UPDATE(status) then
        order_aux := NEW.order_id;

        WITH num_errors as (SELECT COUNT(aux.remainder)
            FROM (SELECT P.stock - OD.quantity as remainder
                FROM products as P, orderdetail as OD
                WHERE OD.orderid = order_aux and OD.prod_id = P.prod_id) as aux
            WHERE aux.remainder <= 0)
        
        if num_errors = 0 then
            --Update inventory and process
            UPDATE
                inventory
            SET stock = remainder
            FROM (SELECT P.stock - OD.quantity as remainder, P.prod_id
                    FROM products as P, orderdetail as OD
                    WHERE OD.orderid = order_aux and OD.prod_id = P.prod_id) as aux
            WHERE inventory.prod_id = aux.prod_id;

            UPDATE
                orders
            SET status = 'PROCESSED'
            WHERE orders.orderid = order_aux;

        else
            --Dont update inventory and alert

        
    return NEW;
end;
$$ language plpgsql;



DROP TRIGGER IF EXISTS upd_inventory ON orders;
CREATE TRIGGER upd_inventory
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE PROCEDURE update_inventory;