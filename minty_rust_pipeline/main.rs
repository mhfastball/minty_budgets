mod src;

fn main() {

    /*first line moves downloaded file to location where file is read and saved into postgres database*/
    src::move_and_copy().ok();

    /*execut sql queries to load and save downloaded transactional data*/
    src::minty_sql().ok();

}

