# minty_budgets

Perosonal pipeline using Rust and Python to parse/engineer and aggregate data downloaded from Intuit Mint application. 

Using downloaded transaction data (in .csv format). Rust will move and parse data into a postgresql database (on localhost).
Then, using python, will query and aggregate data to return if over or under budget. 

Uses a Flask backend with a ReactJS frontend (different repository) that can display a string and table data of current and past budget data.
