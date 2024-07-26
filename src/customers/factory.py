from customers.strategy import JsonProcessing, TxtProcessing, ProcessingStrategy
from rest_framework.exceptions import ValidationError


class ProcessingFactory:
    strategy_map_processing = {"json": JsonProcessing(), "txt": TxtProcessing()}

    @classmethod
    def get_strategy(cls, strategy_name: str):
        return cls.strategy_map_processing.get(strategy_name, None)

    @classmethod
    def processing(cls, strategy_name: str, request):
        strategy: ProcessingStrategy = cls.get_strategy(strategy_name=strategy_name)
        if not strategy:
            raise ValidationError(f"Invalid strategy: {strategy_name}")
        return strategy.processing(request=request)
