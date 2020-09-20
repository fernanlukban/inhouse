class CreateableFromMatchHistory:
    # Override this method to populate new model with information from match_history
    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        pass

    @classmethod
    def from_match_history(cls, match_history, *args, **kwargs):
        new_model = cls(*args, **kwargs)
        cls.setup_from_match_history(match_history, new_model)
        return new_model

    @classmethod
    def create_from_match_history(cls, match_history, *args, **kwargs):
        new_model = cls.from_match_history(cls, match_history, *args, **kwargs)
        new_model.save()
        return new_model


class SidedCreateableFromMatchHistory(CreateableFromMatchHistory):
    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        if "is_blue" not in kwargs:
            raise Exception("Need to pass in is_blue")
        CreateableFromMatchHistory.setup_from_match_history(
            cls, match_history, new_model, *args, **kwargs
        )

    @classmethod
    def setup_from_match_history_sided(
        cls, match_history, blue_new_model, red_new_model
    ):
        cls.setup_from_match_history(match_history, blue_new_model, is_blue=True)
        cls.setup_from_match_history(match_history, red_new_model, is_blue=False)

    @classmethod
    def from_match_history_sided(cls, match_history, *args, **kwargs):
        blue_new_model = cls(*args, **kwargs)
        red_new_model = cls(*args, **kwargs)
        cls.setup_from_match_history_sided(match_history, blue_new_model, red_new_model)
        return blue_new_model, red_new_model

    @classmethod
    def create_from_match_history_sided(cls, match_history, *args, **kwargs):
        blue_new_model, red_new_model = cls.create_from_match_history_sided(
            match_history, *args, **kwargs
        )
        blue_new_model.save()
        red_new_model.save()
        return blue_new_model, red_new_model