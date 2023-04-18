use postgres::{Client, NoTls, Error};
use std::fs;

pub fn minty_sql() -> Result<(), Error> {

    let mut client = Client::connect("postgresql/localhost", NoTls)?;

    client.batch_execute(
        "drop table if exists transact"
    )?;

    client.batch_execute(
        "create temp table transact (
            date date,
            description text,
            original_description text,
            amount double precision,
            transaction_type text,
            category text,
            account_name text,
            labels text,
            notes text
        )"
    )?;
    client.batch_execute(
        "copy transact(date, description, original_description, amount, transaction_type, category, 
        account_name, labels, notes)
        from '/macbook/file/address'
        DELIMITER ','
        csv header"
    )?;

    /*get rid of old table*/
    client.batch_execute(
        "drop table if exists transaction"
    )?;

    client.batch_execute(
        "create table transaction as
            select date, description, original_description, amount, transaction_type, category, account_name
            from transactions
            union ALL
            select date, description, original_description, amount, transaction_type, category, account_name
            from transact"
    )?;

    Ok(())
}


pub fn move_and_copy() -> std::io::Result<()> {
    
    /*go through a directory and find the correct file*/
    /*remove the old file and renames the new downloaded file to the "old" name*/
    let new_file = "/just_downloaded_file.csv";
    let old_file = "/old_named_file.csv";
    let copy_file = "/renamed_old_to_new_file.csv";
    let renamed_file_to_directory = "/directory_plus_renamed_old_to_new_file.csv";

    /*checks if the new downloaded file has been renamed manually already
    if so, then skip and just move file to processing location*/
    if let Ok(metadata) = fs::metadata(new_file) {
        if metadata.is_file() {
            fs::remove_file(old_file)?;
            fs::rename(new_file, copy_file)?;
            fs::copy(copy_file, renamed_file_to_directory)?;
        }
    }
        else {
            fs::copy(copy_file, renamed_file)?;       
    }

    Ok(())

}
