class Pagination:
    def paginate_list(self, data, num_pages=5):
        """
        Метод разбивает список данных на отдельные страницы.
        @param: data(list): Список данных, который требуется разбить на страницы.
        @param:  num_pages(int): Количество элементов на одной странице(по умолчанию 5).
        @return: pages(list): Список страниц, где каждая страница представлена списком элементов.
        """
        total_length = len(data)
        pages = [data[i:i + num_pages] for i in range(0, total_length, num_pages)]
        return pages