grep -c "Resource temporarily unavailable" lb_process.log && grep -c "Connection reset by peer" lb_process.log && grep -c "connecting to" lb_process.log
