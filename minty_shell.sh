#/bin/bash

buddy_one () {
    source /Users/macbook/projects/testing_place/python/new_venv_3.9/bin/activate 
    cd /Users/macbook/projects/testing_place/rust/pipeline 
    cargo run 
    cd  /Users/macbook/projects/testing_place/python/rand_py_scripts/budgets
    python3 minty_flask.py
}

buddy_two () {
    cd '/Users/macbook/projects/testing_place/javascripts/foo_react/foobar'
    npm start
}