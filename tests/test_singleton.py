from asymmetric.singleton import _AsymmetricSingleton


class InstanciatedSingleton(metaclass=_AsymmetricSingleton):
    pass


class TestAsymmetricSingleton:
    def test_singleton_functionality(self):
        first_instance = InstanciatedSingleton()
        second_instance = InstanciatedSingleton()
        assert second_instance is first_instance
