from app.controllers.database.database_controller import DynamoDBController

trades_table = DynamoDBController("ClassicTrades", "trade_id")
orders_table = DynamoDBController("ClassicOrders", "order_id")
pools_table = DynamoDBController("ClassicPools", "instrument_code")
errors_table = DynamoDBController("ClassicErrors", "error_id")
