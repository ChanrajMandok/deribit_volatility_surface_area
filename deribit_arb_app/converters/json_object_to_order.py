from singleton_pattern_decorator.decorator import singleton
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.field_name import FieldName


@singleton
class JsonObjectToOrder:

    def convert(self, json_order) -> ModelOrder:

        web = None
        if FieldName.WEB.value in json_order:
            web = json_order[FieldName.WEB.value]

        time_in_force = json_order[FieldName.TIME_IN_FORCE.value]

        replaced = None
        if FieldName.REPLACED.value in json_order:
            replaced = json_order[FieldName.REPLACED.value]

        reduce_only = json_order[FieldName.REDUCE_ONLY.value]
        profit_loss = json_order[FieldName.PROFIT_LOSS.value]
        price = json_order[FieldName.PRICE.value]
        post_only = json_order[FieldName.POST_ONLY.value]
        order_type = json_order[FieldName.REDUCE_ONLY.value]
        order_state = json_order[FieldName.ORDER_STATE.value]
        order_id = json_order[FieldName.ORDER_ID.value]
        max_show = json_order[FieldName.MAX_SHOW.value]
        last_update_timestamp = json_order[FieldName.LAST_UPDATE_TIMESTAMP.value]
        label = json_order[FieldName.LABEL.value]
        is_liquidation = json_order[FieldName.IS_LIQUIDATION.value]
        instrument_name = json_order[FieldName.INSTRUMENT_NAME.value]
        filled_amount = json_order[FieldName.FILLED_AMOUNT.value]
        direction = json_order[FieldName.DIRECTION.value]
        creation_timestamp = json_order[FieldName.CREATION_TIMESTAMP.value]
        commission = json_order[FieldName.COMMISSION.value]
        average_price = json_order[FieldName.AVERAGE_PRICE.value]
        api = json_order[FieldName.API.value]
        amount = json_order[FieldName.AMOUNT.value]

        if FieldName.TRADES.value in json_order:
            trades = json_order[FieldName.TRADES.value]
        else:
            trades = []

        return ModelOrder(
            web=web,
            time_in_force=time_in_force,
            replaced=replaced,
            reduce_only=reduce_only,
            profit_loss=profit_loss,
            price=price,
            post_only=post_only,
            order_type=order_type,
            order_state=order_state,
            order_id=order_id,
            max_show=max_show,
            last_update_timestamp=last_update_timestamp,
            label=label,
            is_liquidation=is_liquidation,
            instrument_name=instrument_name,
            filled_amount=filled_amount,
            direction=direction,
            creation_timestamp=creation_timestamp,
            commission=commission,
            average_price=average_price,
            api=api,
            amount=amount,
            trades=trades
        )