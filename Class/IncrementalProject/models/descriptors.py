class PositiveNumber:

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):

        if value <= 0:
            raise ValueError("Value must be greater than zero.")

        setattr(instance, self.private_name, value)


class NonEmptyString:

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):

        if not value.strip():
            raise ValueError("String cannot be empty.")

        setattr(instance, self.private_name, value)
