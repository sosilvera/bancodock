# Web de Control

El objetivo de la web es poder obtener información sobre los tickets que estan:
    - Pendientes
    - En ejecución (Taked y Running)
    - Fallidos (Failed, Not Found, etc.)

Además se espera:
    - Poder eliminar un ticket (Solo los que estén Fallidos o Pendientes)
    - Modificar el estado de un ticket

Para esto se necesitan en principio 3 servicios:
    - /getTickets: va a devolver un listado de todos los tickets y sus detalles
    - /updateTicket/{idPedidoEstado, estadoFinal, maquina}: va a modificar el estado de un ticket:
        - De entrada se puede tomar la maquina automaticamente (del llamado a /getTickets), es decir, si estaba en Failed-CREACION01, entonces se vuelve a Pending o Taked o Running de Creacion
        - Si estaba en Failed-DESPLIEGUE01, volver a Pending de DESPLIEGUE:
            - if Pending & DESPLIEGUE01 then Pending & Despliegue
        - En una proxima iteracion se podria preguntar si se quiere crear o desplegar
    - /deleteTicket/<idPedidoEstado>: va a eliminar un ticket