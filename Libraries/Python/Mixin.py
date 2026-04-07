class InspectorMixin:
    @classmethod
    def get_all_map(cls):
        """Возвращает словарь"""
        return {k: v for k, v in cls.__dict__.items()
                if not k.startswith('_') and not callable(v)}

    @classmethod
    def get_all_values(cls):
        """Возвращает только список значений"""
        return list(cls.get_all_map().values())

    @classmethod
    def get_all_names(cls):
        """Возвращает только список имен"""
        return list(cls.get_all_map().keys())


def main():
    pass


if __name__ == "__main__":
    main()
