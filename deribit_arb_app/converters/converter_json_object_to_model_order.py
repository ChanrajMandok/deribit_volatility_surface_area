from singleton_decorator import singleton

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_trade import ModelTrade
from deribit_arb_app.enums.enum_field_name import EnumFieldName

    #################################################
    # Converter Converts Json object to Model Order #
    #################################################

@singleton
class ConverterJsonObjectToModelOrder():

    def convert(self, json_order) -> ModelOrder:

        web = None
        if EnumFieldName.WEB.value in json_order:
            web = json_order[EnumFieldName.WEB.value]

        time_in_force          = json_order[EnumFieldName.TIME_IN_FORCE.value]

        replaced = None
        if EnumFieldName.REPLACED.value in json_order:
            replaced = json_order[EnumFieldName.REPLACED.value]

        reduce_only             = json_order[EnumFieldName.REDUCE_ONLY.value]
        profit_loss             = json_order[EnumFieldName.PROFIT_LOSS.value]
        price                   = json_order[EnumFieldName.PRICE.value]
        post_only               = json_order[EnumFieldName.POST_ONLY.value]
        order_type              = json_order[EnumFieldName.REDUCE_ONLY.value]
        order_state             = json_order[EnumFieldName.ORDER_STATE.value]
        order_id                = json_order[EnumFieldName.ORDER_ID.value]
        max_show                = json_order[EnumFieldName.MAX_SHOW.value]
        last_update_timestamp   = json_order[EnumFieldName.LAST_UPDATE_TIMESTAMP.value]
        label                   = json_order[EnumFieldName.LABEL.value]
        is_liquidation          = json_order[EnumFieldName.IS_LIQUIDATION.value]
        instrument_name         = json_order[EnumFieldName.INSTRUMENT_NAME.value]
        filled_amount           = json_order[EnumFieldName.FILLED_AMOUNT.value]
        direction               = json_order[EnumFieldName.DIRECTION.value]
        creation_timestamp      = json_order[EnumFieldName.CREATION_TIMESTAMP.value]
        commission              = json_order[EnumFieldName.COMMISSION.value]
        average_price           = json_order[EnumFieldName.AVERAGE_PRICE.value]
        api                     = json_order[EnumFieldName.API.value]
        amount                  = json_order[EnumFieldName.AMOUNT.value]

        try:    
            order = ModelOrder(
                web                    = web,
                time_in_force          = time_in_force,
                replaced               = replaced,
                reduce_only            = reduce_only,
                profit_loss            = profit_loss,
                price                  = price,
                post_only              = post_only,
                order_type             = order_type,
                order_state            = order_state,
                order_id               = order_id,
                max_show               = max_show,
                last_update_timestamp  = last_update_timestamp,
                label                  = label,
                is_liquidation         = is_liquidation,
                instrument_name        = instrument_name,
                filled_amount          = filled_amount,
                direction              = direction,
                creation_timestamp     = creation_timestamp,
                commission             = commission,
                average_price          = average_price,
                api                    = api,
                amount                 = amount)

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")

        if EnumFieldName.TRADES.value in json_order:
            for trade_data in json_order[EnumFieldName.TRADES.value]:
                trade = ModelTrade(**trade_data)
                trade.save()
                order.trades.add(trade)
                
        return order