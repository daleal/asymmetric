from asymmetric.singleton import AsymmetricSingleton


class InstanciatedSingleton(metaclass=AsymmetricSingleton):
    pass


class TestAsymmetricSingleton:
    def test_singleton_functionality(self):
        first_instance = InstanciatedSingleton()
        second_instance = InstanciatedSingleton()
        assert second_instance is first_instance
