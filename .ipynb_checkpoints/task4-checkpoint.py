class BankCard:
    def __init__(self, total_sum):
        self.total_sum = total_sum

    def __call__(self, sum_spent):
        if self.total_sum >= sum_spent:
            self.total_sum -= sum_spent
            print('You spent', sum_spent, 'dollars.', self.total_sum, 'dollars are left.')
        else:
            print('Not enough money to spent', sum_spent, 'dollars.')
            raise ValueError()

    def __repr__(self):
        return 'To learn the balance you should put the money on the card, spent some money or get the bank data. The last procedure is not free and costs 1 dollar.'

    @property
    def balance(self):
        if self.total_sum >= 1:
            self.total_sum -= 1
            return self.total_sum
        else:
            print('Not enough money to learn the balance.')
            raise ValueError()

    def put(self, sum_put):
        self.total_sum += sum_put
        print('You put', sum_put, 'dollars.', self.total_sum, 'dollars are left.')

