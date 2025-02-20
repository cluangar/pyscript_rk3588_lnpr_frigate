# pyscript_rk3588_lnpr_frigate
Extend repository https://github.com/cluangar/pyscript_simple_lnpr_frigate only use on RK3588
Link https://github.com/cluangar/pyscript_simple_lnpr_frigate

# Prerequisites
1. LNPR API: docker pull cluangar/rk3588_lnpr_frigate

# Example Run Docker
docker run --rm --privileged \
-p 8001:8001 \
--device /dev/dri \
--device /dev/rknpu \
cluangar/rk3588_lnpr_frigate

# Example Run create api to call lnpr api
python test_api.py -id <event_id> -fip <frigate ip> -fp 5000 -aip <lnpr_api ip> -ap <lnpr_api port>

![example1](https://github.com/user-attachments/assets/e4279989-87d5-4f2f-bcfa-545674859a03)
![example2](https://github.com/user-attachments/assets/194511bb-db35-432f-98f6-d962038f1d6d)

curl -X POST "http://<lnpr_api>:8001/alpr/" -H "Content-Type: application/json" -d '{"url": "https://github.com/user-attachments/assets/e4279989-87d5-4f2f-bcfa-545674859a03", "h_url": "https://github.com/user-attachments/assets/e4279989-87d5-4f2f-bcfa-545674859a03", "filename": "1740051950.935343-test.jpg", "cam_user": "", "cam_pass": "", "url_frigate_events": "", "broker_address": "", "mqtt_user": "", "mqtt_pass": ""}' -v

