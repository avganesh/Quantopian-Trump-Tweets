"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume
from quantopian.pipeline.filters.morningstar import Q500US
 
def initialize(context):
    """
    Called once at the start of the algorithm.
    """   
    context.VIX = sid(40670)
    fetch_csv('https://dl.dropboxusercontent.com/u/4695582/data.csv',
              pre_func=None, 
              post_func=None, 
              date_column='Date', 
              date_format='%Y-%m-%d', 
              timezone='UTC', 
              symbol='DT'
             )
    
    # Rebalance every day, 1 hour after market open.
    schedule_function(my_rebalance, date_rules.every_day(), time_rules.market_open(hours=1))
     
    # Record tracking variables at the end of each day.
    schedule_function(my_record_vars, date_rules.every_day(), time_rules.market_close())
    
    # Create our dynamic stock selector.
    #attach_pipeline(make_pipeline(), 'my_pipeline')
         
def make_pipeline():
    """
    A function to create our dynamic stock selector (pipeline). Documentation on
    pipeline can be found here: https://www.quantopian.com/help#pipeline-title
    """
    
    # Base universe set to the Q500US
    base_universe = Q500US()

    # Factor of yesterday's close price.
    yesterday_close = USEquityPricing.close.latest
     
    pipe = Pipeline(
        screen = base_universe,
        columns = {
            'close': yesterday_close,
        }
    )
    return pipe
 
def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    #context.output = pipeline_output('my_pipeline')
    
    # These are the securities that we are interested in trading each day.
    #context.security_list = context.output.index
    pass
    
def my_assign_weights(context, data):
    """
    Assign weights to securities that we want to order.
    """
    pass
 
def my_rebalance(context,data):
    """
    Execute orders according to our schedule_function() timing. 
    """
    if data.can_trade(context.VIX) and 'count' in data['DT']: 
#        if data.current('DT', 'count') > data.current('DT', 'rolling mean'):
        if 10*data.current('DT', 'Sentiment Polarity') +2 < 0:
            order_target_percent(context.VIX, 1)
            print('Donald Tweeted ', data.current('DT', 'count'), ' times today.')
#        elif data.current('DT', 'count') < data.current('DT', 'rolling mean'):
        elif 10*data.current('DT', 'Sentiment Polarity') -2 > 0:
            order_target_percent(context.VIX, -1)
 
def my_record_vars(context, data):
    """
    Plot variables at the end of each day.
    """
    if 'count' in data['DT']:
        record(DonaldTweetCount=data.current('DT', 'count'))
        record(DonaldTweetMean=data.current('DT', 'rolling mean'))
        record(DonaldTweetSentiment=10*data.current('DT', 'Sentiment Polarity'))
 
def handle_data(context,data):
    """
    Called every minute.
    """
    pass
