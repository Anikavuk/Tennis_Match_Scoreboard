
class Pagination:
    def paginate_list(self, data, num_pages=5):
        total_length = len(data)
        number_of_pages = total_length // num_pages
        remainder = total_length % num_pages
        base = 0
        if remainder ==0:
            base=number_of_pages
        else:
            base = number_of_pages+1
        pages = []
        start_index = 0

        for i in range(base):
            current_page_size = num_pages
            page = data[start_index:(start_index + current_page_size)]
            pages.append(page)
            print(len(page))
            start_index += current_page_size

        return pages

fff = [ {'player1': '2', 'player2': 'ty', 'winner': 'io'}, {'player1': '3', 'player2': 'ui', 'winner': 'ui'}, {'player1': '4', 'player2': 'rt', 'winner': 'ty'}, {'player1': '5', 'player2': 'ui', 'winner': 'ty'},
        {'player1': '1', 'player2': 'rt', 'winner': 'io'}, {'player1': '2', 'player2': 'ty', 'winner': 'io'}, {'player1': '3', 'player2': 'ui', 'winner': 'ui'}, {'player1': '4', 'player2': 'rt', 'winner': 'ty'}, {'player1': '5', 'player2': 'ui', 'winner': 'ty'}]
aaa = Pagination()
print(aaa.paginate_list(fff))
print(len(fff))
remainder = len(fff) % 5
print(remainder)