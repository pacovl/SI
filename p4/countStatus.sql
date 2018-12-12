-- primera consulta
select count(*)
from orders
where status is null;

-- segunda consulta
explain select count(*)
from orders
where status ='Shipped';

-- creacion indice
create index idx_status on orders(status);
-- generacion estadisticas
analyze orders;

-- planes de ejecucion las consultas
explain select count(*)
from orders
where status is null;

explain select count(*)
from orders
where status ='Shipped';
