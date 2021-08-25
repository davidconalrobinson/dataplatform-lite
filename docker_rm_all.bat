docker container stop dataplatform-lite-db-infra
docker container stop dataplatform-lite-db-src
docker container stop dataplatform-lite-viz
docker container stop dataplatform-lite-api
docker container rm dataplatform-lite-db-infra
docker container rm dataplatform-lite-db-src
docker container rm dataplatform-lite-viz
docker container rm dataplatform-lite-api
docker image rm xero-case-study_db_infra
docker image rm xero-case-study_db_src
docker image rm xero-case-study_viz
docker image rm xero-case-study_api
pause