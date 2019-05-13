from Society import *
law_book = Society.load_law_book('./', 'law_book')
society = Society(law_book, size=(150, 150))
Society.visualize(society, 500)
