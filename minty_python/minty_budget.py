from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import calendar
import json


class MintyFresh:
    '''query for one line print out. finds the max transaction within a month and returns it'''
    one_line_string = '''select * 
        from public.transaction
        where date_part('year', date) in (2023)
        and account_name in (bunch_of_accounts)
        and transaction_type = 'debit'
        and date_part('month', date) = (select max(date_part('month', date)) 
                                            from public.transaction 
                                                where date_part('year', date) in (2023))
        '''
    '''query for a whole table to see month to month budget over/under'''
    table_query = """select * 
        from public.transaction
        where date_part('year', date) in (2023)
        and account_name in (bunch_of_accounts)
        and transaction_type = 'debit'
        """

    def __init__(self):
        self.home = create_engine("postgres/localhost")

    '''function to pull and engineer sql data'''
    def minty_data(self, query):
        df = pd.read_sql_query(query, con=self.home, index_col=None)
        df = df.drop_duplicates()
        df['year'] = df.date.dt.year
        df['month'] = df.date.dt.month
        df['date'] = df.date.dt.day
        dfg = df.groupby(['month'], as_index=False)['amount'].sum()
        dfg.sort_values(['month'], inplace=True)
        #dfg.reset_index(inplace=True, drop=True)
        return df, dfg
    

    '''both functions adds a over/under column for monthly budget checking'''
    def over_under(self, spent, budget):
        if spent < budget:
            return 'okay'
        else:
            return 'over budget: ' + str(budget - spent) 
        
    def minty_table(self, query, budget):
        df, dfg = self.minty_data(query)
        dfg['over_under'] = [self.over_under(spent, budget) for spent in dfg.amount]
        return df, dfg


    '''aggregates/engineers a table for historical budget checking as well as a one line string of current status'''
    def minty_printout(self, query, first_threshold, second_threshold):
        df, dfg = self.minty_data(query)
        latest_month = df.month.max()
        latest_year = df.year.max()
        latest_day = df.date.max()
        month_days = calendar.monthrange(latest_year, latest_month)[1]
        amount_over = dfg.amount.sum() - first_threshold
        amount_left = first_threshold - dfg.amount.sum()
        days_left =  month_days - latest_day
        under = amount_left/days_left
        #over = amount_over/days_left
        dfg = dfg[dfg.month == latest_month]
        over_text = 'Over budget by: ' + str(amount_over) + ' with ' + str(days_left) + " days left. Cut Back"
        under_text = 'We good. Have left: ' + str(amount_left) + ' with ' + str(days_left) + ' days left. About ' + str(under) + ' left per day'
        if dfg.amount.sum() > second_threshold:
            print(over_text)
            return over_text
        else:
            print(under_text)
            return under_text


'''variables for export into backend flask'''
ols = MintyFresh().one_line_string
tq = MintyFresh().table_query
personal = MintyFresh().minty_printout(ols, 3000, 5000)
source, monthly_dict = MintyFresh().minty_table(tq, 3000)
jsoning = monthly_dict.to_json(orient='records')
flask_json = json.loads(jsoning.replace("'", "\""))