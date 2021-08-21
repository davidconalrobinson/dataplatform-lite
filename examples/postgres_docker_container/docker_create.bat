docker run --name xero-case-study-db ^
    -e HOSTNAME=xero-case-study-db ^
    -e POSTGRES_PASSWORD=postgres ^
    -e POSTGRES_USER=postgres ^
    -e POSTGRES_DB=xero-case-study-db ^
    -p 5432:5432 ^
    -d postgres ^
    -c track_commit_timestamp=on
pause