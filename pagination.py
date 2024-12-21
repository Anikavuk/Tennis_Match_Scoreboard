class Pagination:
    def paginate_list(self, data, num_pages=5):
        total_length = len(data)
        pages = [data[i:i + num_pages] for i in range(0, total_length, num_pages)]
        return pages