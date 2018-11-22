drop function if exists set_order_amount() cascade;
create function set_order_amount()
returns void AS $$

begin
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
    return;
end;
$$ language plpgsql;
